"""
Este arquivo tem como função definir os nós de declaração: programa, funções, parâmetros e variáveis. Programa é a raiz da AST.

Entrada/Saída: nenhuma (aqui só tem classes dos nós)
Depende de: ast_comandos.py, ast_expressoes.py

Programa: nome, variáveis, funções, comandos.
DeclFuncao: nome, parâmetros, tipo de retorno, variáveis, funções aninhadas, comandos.
Parametro: tipo, nome.
DeclVar: tipo, nome, inicialização opcional.
Anotação simbolo nas declarações.

object é usado para simbolo, para não criar outra dependencia

"""



from __future__ import annotations
from dataclasses import dataclass

from arvore_sintatica.ast_expressoes import No, Expr
from arvore_sintatica.ast_comandos import Cmd




@dataclass
class Programa(No):
    """
    Classe para a raiz da AST (o programa como um todo).
    """
    nome: str
    variaveis: list[DeclVar]
    funcoes: list[DeclFuncao]
    comandos:list[Cmd]
    simbolo: object | None = None

@dataclass
class DeclFuncao(No):
    """
    Classe para declaração de função na AST.
    """
    nome: str
    parametros: list[Parametro]
    tipo_retorno: str
    variaveis: list[DeclVar]
    funcoes: list[DeclFuncao]
    comandos: list[Cmd]
    simbolo: object | None = None

@dataclass
class Parametro(No):
    """
    Classe para um parâmetro de função na AST.
    """
    tipo: str
    nome: str
    simbolo: object | None = None

@dataclass
class DeclVar(No):
    """
    Classe para uma declaração de variável na AST.
    """
    tipo: str
    nome: str
    inicializacao: Expr | None = None
    simbolo: object | None = None


