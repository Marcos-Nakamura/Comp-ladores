"""
    Esse arquivo tem como função centralizar o registro e a exibição de todos os erros do compilador, para que todas as áreas reportem da mesma 
    forma e o compilador saiba como prosseguir

    Entrada: fase, linha e mensagem
    Saída: a lista de erros e um bool para "houve erro?" 
"""

#Imports

from dataclasses import dataclass #serve para criar a classe erro

import sys #serve para fazer chamadas de erro

#Lista de erros

"""
    Primeiro foi criada uma classe de erro para orientar os dados que cada erro deve conter e depois foi criada uma lista a qual vai guardar os
    erros
"""

@dataclass
class Erro:
    fase: str
    linha: int  |None
    msg: str

lista_erros: list[Erro] = []

#Registrar

def registra(fase: str, linha: int|None, mensagem: str):
    """
        Aqui o arquivo recebe os parâmetros do erro e registra na lista
    """
    err = Erro(fase, linha, mensagem)

    lista_erros.append(err)

#Verificar erros

def tem_erro():
    """
        Apenas retorna um bool, sendo true caso a lista tenha erros, e false caso a mesma esteja vazia
    """
    return len(lista_erros) > 0

#Formatação dos erros

def formatar(err: Erro):
    """
        Essa função serve para montar a string do erro, e emiti-la dessa, com um adendo que se não houver linha (em caso de fim inesperado do arquivo
        por exemplo), tem uma string um pouco diferente
    """
    if err.linha is None:
        return f"ERRO {err.fase}: {err.msg}"


    return f"ERRO {err.fase} na linha {err.linha}: {err.msg}"


#Impressão

def imprime_tudo():
    """
        Essa função imprime todos os erros de acordo com a ordem de colocação deles na lista
    """
    for e in lista_erros:
        print (formatar(e), file=sys.stderr)

#Limpar lista

def limpa():
    """
        Essa função existe apenas para fins de testes caso necessário, ao trabalhar com varios arquivos
    """
    lista_erros.clear()