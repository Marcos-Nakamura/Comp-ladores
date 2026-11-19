'''
A testar

Entrada: Nenhuma.
Saída: Classe dos nós de expressão e classes-base, usados pelo parser, semântico e gerador.
Depende de: apenas bibliotecas padrões do Python
'''
from dataclasses import dataclass, field
from typing import Any

@dataclass
class No:
    """
    Classe base de todos os nós da AST.
    Linha é obrigatoriamente o primeiro argumento posicional.
    """
    linha: int 

@dataclass
class Expr(No):
    """
    Classe base de nós que representam expressões.
    kw_only=True é usado para que os campos tanham valores padrão sem causar problemas na herança dos dataclasses.
    """
    tipo: Any = field(default=None, kw_only=True)

@dataclass
class OpBinario(Expr):
    operador: str
    esquerda: Expr
    direita: Expr

@dataclass
class OpUnario (Expr):
    operador: str
    operando: Expr

@dataclass
class Numero(Expr):
    valor: int

@dataclass
class Booleano(Expr):
    valor: bool

@dataclass
class Id(Expr):
    nome: str
    simbolo: Any = field(default=None, kw_only=True)

@dataclass
class Chamada(Expr):
    '''
    default_factory garante que cada chamada tenha sua própria lista de argumentos,
    evitando o compartilhamento de listas entre instâncias
    '''
    nome: str
    argumentos: list[Expr] = field(default_factory=list)
    simbolo: Any = field(default=None, kw_only=True)