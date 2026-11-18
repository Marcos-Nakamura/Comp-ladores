"""
    Esse arquivo tem a função de teste das árvores ASTs, ele pega a árvore que o parser montou imprime de forma a ser visualizada
    
    Dessa forma, nenhum outro arquivo depende dele, ele não é essencial para o funcionamento, porém importante para a testagem

    Entrada : um nó da AST (normalmente a raiz, Programa)
    Saída   : texto, um nó por linha, recuado por profundidade
"""

#Imports

from dataclasses import is_dataclass

#Constantes

ESPACOS_POR_NIVEL = 2

#Função pública (A única a ser chamada por outros arquivos)

def imprime_ast(raiz):
    """
        Aqui eu apenas abro os conjuntos e chamo a funcao de impressao
    """
    linhas = [] #cada linha vai sendo adicionada aqui
    abertos = set() #nos que estão sendo impressos

    _imprime(raiz, 0, linhas, abertos)

    return "\n".join(linhas)

#Função auxiliar

def _e_no(valor):
    """
        is_dataclass verifica e da True para a classe  e para uma instancia dela. como quero a instancia entao excluo  quem é type
    """
    return is_dataclass(valor) and not isinstance(valor, type)

def _imprime(valor, nivel, linhas, abertos):
    """
        Aqui é feita a impressao mesmo das linhas
    """
    recuo = " " * (nivel * ESPACOS_POR_NIVEL) # quantos espaços antes da linha  deste falor

    filho = recuo +  " " * ESPACOS_POR_NIVEL # quantos espaços antes da linha dos campos dele (um a mais q o cabeçalho)

    # caso 1 - é um nó de ast
    if _e_no(valor):
        nome = type(valor).__name__ # nome da classe

        """
            Se este nó ja está aberto, estamos voltando para ele por um caminho circular. Escrevo um caminho e paro para nao entrar em recursão 
            infinita
        """
        if id(valor) in abertos:
            linhas.append(recuo + "<ciclo: " + nome + ">")
            return
        abertos.add(id(valor)) # marca o nó que está sendo impresso

        linhas.append(recuo + nome + " (linha " + str(valor.linha) + ")") # cabeçalho

        """
            vars() devolve {campo: conteudo} de TUDO que está no nó, inclusive o que a semantica anotar posteriormente
        """
        for campo, conteudo in vars(valor).items():
            if campo == "linha":
                continue #ja saiu do cabeçalho

            if _e_no(conteudo) or isinstance(conteudo, list):
                # Tem filhos: escrevo só o nome do campo e desço DOIS níveis
                linhas.append(filho + campo + ":") 
                _imprime(conteudo, nivel + 2, linhas, abertos)
            else:
                """
                Valor simples ou None: cabe na mesma linha. repr() mostra
                'x' com aspas e 10 sem, distinguindo texto de número.
                """
                linhas.append(filho + campo + ": " + repr(conteudo))
            
        abertos.discard(id(valor)) #terminei de imprimir e agora desmarco pois não corro mais risco de ciclos   
    # caso 2 - é uma lista
    elif isinstance(valor, list):
        if not valor:
            """
                Lista vazia tem que aparecer
            """
            linhas.append(recuo + "(vazio)")
        else:
            for item in valor:
                _imprime(item, nivel, linhas, abertos) # MESMO nível: a lista não cria recuo, cada item já é um nó
    
    # caso 3 - qualquer outra coisa
    else:
        linhas.append(recuo + repr(valor))