"""
    Esse arquivo faz a verificação semântica de todos os comandos da linguagem: atribuição, if/else.....ente

    Entrada: um nó de comando e o contexto(tabela de símbolos, função atuall e atalho de erro)
    Saída: nenhuma; erros são registrados em erros.py e o que estiver certo o programa faz anotações na AST
"""

#Imports

from analisador_semantico.tipos_regras import BOOL, ERRO # INT não é usado aqui, por isso não foi trazido
from analisador_semantico.sem_expressoes import analisar_chamada_como_comando

#Constantes

VOID = "void" # Apenas um indicador para funções sem retorno

#Funções auxiliares

def _valor(no_expr, contexto):
    """
        Visita uma espressão cujo resultado necessita de valor como por exemplo, atribuição, condição, etc. E recusa 
        função void, registrando ERRO, nesse caso, apenas ChamadaCmd não a usa, pois lá retornar void é permitido
    """
    tipo = contexto.visitar(no_expr) 

    if tipo == VOID:
        contexto.erro(no_expr.linha, "void não pode ser usado como valor")
        return ERRO
    
    return tipo

def _confere_condicao(no, nome, contexto):
    """
        Essa função confere a condição de um if ou de um while e se a condição não for bool, registra erro
    """
    tipo = _valor(no.condicao, contexto)

    if tipo != ERRO and tipo != BOOL:
        contexto.erro(no.linha, "a condição de " + nome + " deve ser bool, e não " +  tipo)

#Função de atribuição

def visita_Atrib(no, contexto):
    """
        Essa função verifica a atribuição (x = expr), onde Sem_expressao cuida de reportar se ele foi decalaradou ou não é
        uma variável. Após isso a expressão é visitada como valor e o itpo da mesma deve ser igual ao da variável.
        Se um dos dois já deu erro, a comparação nem é feita
    """
    tipo_var = contexto.visitar(no.variavel)
    tipo_expr = _valor(no.expressao, contexto)
    if tipo_var != ERRO and tipo_expr != ERRO and tipo_var != tipo_expr:
        contexto.erro(no.linha, "atribuição incompatível: variavel é " + tipo_var + " e expressao é " + tipo_expr)

#Funções condicionais

def visita_If(no, contexto):
    """
        Essa função verifica o if. confere se a condição é bool e visita os comandos do bloco "então". se houver else, ele é visitado
        por visita_Else, caso não haja, não acontece nada
    """
    _confere_condicao(no, "if", contexto)

    for comando in no.entao:
        contexto.visitar(comando)
    contexto.visitar(no.senao) # sem else não cria escopo

def visita_Else(no, contexto):
    """
        Apenas visita os comandos do bloco, pois as verificações necessárias ja foram fitas no visita_if
    """
    for comando in no.comando:
        contexto.visitar(comando)

#Função de repetição

def visita_While(no, contexto):
    """
        Essa função verifica o while, confere que a condição é vool e visitaos comandos do bloco, assim como o if
    """
    _confere_condicao(no, "while", contexto)
    for comando in no.execucao:
        contexto.visitar(comando)

#Funções de leitura e escrita

def visita_Read(no, contexto):
    """
        Essa função verifica o read, só visiando caa variavel da lista com um Id comum, sem_expressoes reporta
        se algum nome nao foi declarado ou não é variavel, como variavel é só de tipo bool ou int, não há nada mais
        a ser verificado
    """
    for id in no.variaveis:
        contexto.visitar(id)

def visita_Print(no, contexto):
    """
        Verifica o print. Cada expressão é visitada como valor, então void aqui dentro retorna erro
    """
    for expr in no.expressoes:
        _valor(expr, contexto)

#Função de chamada como comando

def visita_ChamadaCmd(no, contexto):
    """
        Essa função verifica uma chamada usacda como comando, como por exemplo "f(3);" e sem_expressões confere.
        Aqui a função void é permitida
    """
    analisar_chamada_como_comando(no.chamada, contexto)

#Função de retorno

def visita_Return(no, contexto):
    """
        Essa função verifica o return, conformem a função atual que vem do contexto. Então ela da erro se o return estiver
        fora da função, se falta o valor em função unit ou bool, ou se há vallor em função void, ou se o tupo do valor é diferente
        do tipo de retorno.

        Quando está tudo certo, marca "tem_return", na função atual o que sem_declarações usa para conferir se a função retorna o valor
    """
    funcao = contexto.funcao_atual

    if funcao is None: 
        contexto.erro(no.linha, "return fora de função")
        contexto.visitar(no.expressao) #visita ainda assim para achar erros dentro dela
        return

    if no.expressao is None:
        if funcao.tipo_retorno != VOID:
            contexto.erro(no.linha, "função " + funcao.tipo_retorno + " precisa retornar um valor")

        return    

    if funcao.tipo_retorno == VOID:
        contexto.visitar(no.expressao) #visita só para achar erros dentro dela
        contexto.erro(no.linha, "função void não pode retornar valor")
        
        return

    tipo = _valor(no.expressao, contexto)

    funcao.tem_return = True 
    if tipo!= ERRO and tipo != funcao.tipo_retorno:
        contexto.erro(no.linha, "return do tipo " + tipo + ", esperado " + funcao.tipo_retorno)

    