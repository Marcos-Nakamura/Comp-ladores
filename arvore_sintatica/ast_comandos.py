"""
    Este arquivo tem como função definir os tipos de nós que representam os comandos do programa na AST:

    - atribuição
    - if 
    - while
    - return
    - read
    - print
    - chamada

    Entrada: nenhuma (aqui só tem definições de chamadas)
    Saída: as classes dos nós de comando
"""

#Imports

from __future__ import annotations #para fazer anotação de tipos

from arvore_sintatica.ast_expressoes import No, Expr, Id, Chamada #apenas importando tipos definidos anteriormente

from dataclasses import dataclass, field #serve para criar as classes

#Definições
"""
    Aqui eu faço as definições
"""

@dataclass
class Cmd(No):
    """
        Apenas marca que o nó é um comando, para usar em outros tipos
    """
    pass

@dataclass
class Atrib(Cmd):
    """
        Aqui eu defino a atribuição de variáveis e o que é necessário para a mesma
    """
    variavel: Id
    expressao: Expr

@dataclass
class If(Cmd):
    """
        Aqui eu defino o "if" e suas condições, como senão é opcional então precisa de um valor padrão, uma lista vazia
        Como o python não deixa escrever "= []" direto eu uso o "(default_factory=list)" para resolver isso
    """
    condicao: Expr
    entao: list[Cmd]
    senao: list[Cmd] = field(default_factory=list)

@dataclass
class While(Cmd):
    """
        Aqui eu defino o "while"
    """
    condicao: Expr
    execucao: list[Cmd]

@dataclass
class Return(Cmd):
    """
        Aqui eu defino o "return", o None é o valor padrão que faz com que funções de retorno void funcionem
    """
    expressao: Expr|None = None

@dataclass
class Read(Cmd):
    """
        Aqui eu defino o "read", que guarda uma lista de variaveis
    """
    variaveis: list[Id]

@dataclass
class Print(Cmd):
    """
        Aqui eu defino a classe print
    """
    expressoes: list[Expr]

@dataclass
class ChamadaCmd(Cmd):
    """
        Aqui eu apenas embrulho o nó chamada para usar como comando, como por exemplo fat(5)
    """
    chamada: Chamada