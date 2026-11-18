"""
    Este arquivo tem como função escrever as regras do PLY (BNF) dos comandos da linguagem, montando os nós de ast_comandos

    Entrada: tokens(via PLY) e as regras de expressões
    Saída: nós de comandos e listas Python de comandos
"""

#Imports

from analisador_lexico.tokens import tokens #importo a lista de tokens

from arvore_sintatica.ast_expressoes import Id #importo as expressões

from arvore_sintatica.ast_comandos import Atrib, If, Else, While, Return, Read, Print, ChamadaCmd #importo os comandos de ast_comandos

#Comandos

def p_comando(p):
    """
        comando : atribuicao 
                | condicional 
                | repeticao 
                | retorno 
                | leitura 
                | escrita 
                | chamada_cmd
    """
    
    p[0] = p[1]

def p_lista_comandos(p):
    """
        comandos : comandos comando 
                 | empty
    """
    if len(p) == 3:
        p[0] = p[1] + ([p[2]] if p[2] is not None else [])
    else:
        p[0] = []

#Atribuição

def p_atribuicao(p):
    """
        atribuicao : IDENT ATRIB expressao PONTO_VIRG
    """
    p[0] = Atrib(variavel = Id(nome = p[1], linha = p.lineno(1)), expressao = p[3], linha = p.lineno(1))
    
#Condicional

def p_condicional(p):
    """
        condicional : IF ABRE_PAREN expressao FECHA_PAREN ABRE_CHAVE comandos FECHA_CHAVE
                    | IF ABRE_PAREN expressao FECHA_PAREN  ABRE_CHAVE comandos FECHA_CHAVE ELSE ABRE_CHAVE comandos FECHA_CHAVE
    """
    if len(p) == 12:
        p[0] = If(condicao = p[3], entao = p[6], senao=Else(comando=p[10], linha=p.lineno(8)), linha = p.lineno(1))
    else: 
        p[0] = If(condicao = p[3], entao = p[6], linha = p.lineno(1))

#Repetição

def p_repeticao(p):
    """
        repeticao : WHILE ABRE_PAREN expressao FECHA_PAREN ABRE_CHAVE comandos FECHA_CHAVE
    """
    p[0] = While(condicao = p[3], execucao = p[6], linha = p.lineno(1))

#Retorno

def p_retorno(p):
    """
        retorno : RETURN expressao PONTO_VIRG
                | RETURN PONTO_VIRG
    """
    if len(p) == 4:
        p[0] = Return(expressao = p[2], linha = p.lineno(1))
    else:
        p[0] = Return(linha = p.lineno(1))

#Leitura e Escrita

def p_leitura(p):
    """
         leitura : READ ABRE_PAREN lista_identificadores FECHA_PAREN PONTO_VIRG
    """
    p[0] = Read(variaveis = p[3], linha = p.lineno(1))

def p_lista_identificadores(p):
    """
        lista_identificadores : lista_identificadores VIRGULA IDENT
                              | IDENT
    """
    if len(p) == 4:
        p[0] = p[1] + ([Id(nome = p[3], linha = p.lineno(3))]  if p[3] is not None else [])
    else:  
        p[0] = [Id(nome=p[1], linha=p.lineno(1))]


def p_escrita(p):
    """
        escrita : PRINT ABRE_PAREN lista_expressoes FECHA_PAREN PONTO_VIRG
    """
    p[0] = Print(expressoes = p[3], linha = p.lineno(1))

def p_lista_expressoes(p):
    """
        lista_expressoes : lista_expressoes VIRGULA expressao
                         | expressao
    """
    if len(p) == 4:
        p[0] = p[1] + ([p[3]] if p[3] is not None else [])
    else:
        p[0] = [p[1]]

#Chamada como comando

def p_chamada_cmd(p):
    """
        chamada_cmd : chamada PONTO_VIRG
    """
    p[0] = ChamadaCmd(chamada = p[1], linha =  p[1].linha)