"""
    Este arquivo gera o código MEPA de todos os comandos da linguagem: atribuição, if/else, while, read, print, chamada como comando e return.
    Ele não consulta a tabela de símbolos: ele apenas lê o que a semântica deixou nos nós (símbolo e tipo)

    Entrada: um nó de comando já anotado e o contexto da geração
    Saídas: nenhuma; as instruções saem em saída.emissor
"""

#Atribuição

def visita_Atrib(no, contexto):
    """
        Gera o código da atribuição, primeiro gera a expressão, o que deixa o valor no topo da pilha, e depois o grava na variavel com ARMZ, usando
        o nível e o deslocamento que a semântica anotou
    """
    contexto.visitar(no.expressao) #deixa o valor no topo da pilhas
    s = no.variavel.simbolo #anotado pela semântica
    contexto.emissor.emite("ARMZ", s.nivel, s.deslocamento)

#Condicionais

def visita_If(no, contexto):
    """
        Gera o código do if, gerando a condição, a qual deixa 0 ou 1 no topo da lista, e usa DFVS para pular o bloco quando for falsa, sem else o
        desvio vai para o fim do if, caso tenha else o desvio vai para o início de else
    """
    e = contexto.emissor
    contexto.visitar(no.condicao) #deixa 0 ou 1 no topo
    if no.senao is None:
        fim = e.novo_rotulo()
        e.emite("DSVF", fim) #se falso, pula o bloco todo
        for comando in no.entao:
            contexto.visitar(comando)
        e.marca(fim)
    else:
        rotulo_else = e.novo_rotulo()
        fim = e.novo_rotulo()
        e.emite("DSVF", rotulo_else) #agora, se falso, pula para o bloco else
        for comando in no.entao:
            contexto.visitar(comando)
        e.emite("DSVS", fim) #terminou o então, logo pula o else
        e.marca(rotulo_else)
        contexto.visitar(no.senao) #chama o visita_else
        e.marca(fim)

def visita_Else(no, contexto):
    """
        Apenas gera os comandos do bloco else, esta função está aqui mais por questão de padronização
    """
    for comando in no.comando:
        contexto.visitar(comando)

#While

def visita_While(no, contexto):
    """
        Gera o código do while, marcando o rótulo de início, gera a condição e usa um DSVF para saír do laço. E depois do corpo volta ao início com
        um DSVS
    """
    e =  contexto.emissor
    inicio = e.novo_rotulo()
    fim = e.novo_rotulo()
    e.marca(inicio)
    contexto.visitar(no.condicao)
    e.emite("DSVF", fim)
    for comando in no.execucao:
        contexto.visitar(comando)
    e.emite("DSVS", inicio)
    e.marca(fim)

#Leitura e Escrita

def visita_Read(no, contexto):
    """
        Gera o código do read. para cada variavel da lista, lê um valor com LEIT, que o empilha e o grava na variável com ARMZ, usando o nível de
        deslocamento anotado no id
    """
    for id in no.variaveis:
        contexto.emissor.emite("LEIT")
        s = id.simbolo
        contexto.emissor.emite("ARMZ", s.nivel, s.deslocamento)

def visita_Print(no, contexto):
    """
        Gera o código do print, onde para cada expressão da lista, gera a expressao e a imprime com IMPR, cada expressão é impressa separadamente
    """
    for expressao in no.expressoes:
        contexto.visitar(expressao)
        contexto.emissor.emite("IMPR")

#Chamada como comando

def visita_ChamadaCmd(no, contexto):
    """
        Gera o código de uma chamada como comando, como "f(3)". Quem emite a chamda em si é ger_expressoes. Aqui só se descarta o valor: se a função
        não for void, ela deixou um resultado no topo da pilha, e DMEM 1 o remove
    """
    contexto.visitar(no.chamada)
    if no.chamada.tipo != "void":
        contexto.emissor.emite("DMEM", 1)

#Retorno 

def visita_Return(no, contexto):
    """
        Gera o código do return conforme a função atual, a qual vem do contexto. Com o valor, gera a expressão e a grava no espaço de retorno com
        ARMZ na posição -(5 + n) sendo n o número de parametros. depois termina com um DSVS para o rótulo de fim de função
    """
    funcao = contexto.funcao_atual
    if no.expressao is not None:
        contexto.visitar(no.expressao)
        n = len(funcao.parametros) #numero de parâmetros
        k = funcao.simbolo.nivel #nivel lexico da função
        contexto.emissor.emite("ARMZ", k, -(5 + n))
    contexto.emissor.emite("DSVS", funcao.rotulo_fim)