"""
    Basicamente esse arquivo coordena toda a fase semântica, garantindo que cada fase funcione devidamente e dando retorno ao programa principal
    quem faz o trabalho real são os modulos, que são os outros três arquivos semanticos

    Entrada: a raiz da AST
    Saída: nada, esse arquivo deixa as anotações na AST, logo não retorna nada
"""

#Imports 

from __future__ import annotations

import erros

from analisador_semantico.tabela_simbolos import TabelaSimbolos

from analisador_semantico import sem_expressoes, sem_comandos, sem_declaracoes

#Constante

"""
    Os modulos são so arquivos especializados para cada tipo de nó, sendo expressoes, comandos e declarações, eles são salvos numa tupla, para evitar
    reetição de código, e por não precisarem ser alterados
"""
MODULOS = (sem_expressoes, sem_comandos, sem_declaracoes)

#Contexto

class Contexto:
    """
        Essa classe guarda a tabela de símbolos e a função que está sendo analisada, as quais serão compartilhadas por todas as visitas
    """
    def __init__(self):
        self.tabela = TabelaSimbolos()
        self.funcao_atual = None

    def visitar(self, no):
        """
            Essa função recebe um nó da AST e chama a função certa para o mesmo
        """
        if no is None:
            return #retorna vazio para caso receba entrada vazia

        nome = type(no).__name__
        funcao = None

        for mod in MODULOS:
            """
                Esse laço encontra qual seu módulo correto e para assim que encontrar, caso não encontre, ele retorna como none mesmo
            """
            funcao = getattr(mod, "visita_" + nome, None)
            if funcao is not None:
                break

        if funcao is None:
            raise NotImplementedError(f"visita_{nome} não foi implementada.")

        return funcao(no, self)   # retorna o nó e o próprio contexto

    def erro(self, linha, mensagem):
        erros.registra("SEMÂNTICO", linha, mensagem)

#Função pública (a unica que nesti.py acessa)

def analisa(raiz):
    contexto = Contexto()
    contexto.visitar(raiz)   # o visita_Programa desce pelo resto

    #não devolve nada, uma vez que o verifica_erros() do nesti.py verifica isso e decide continuar ou não


    