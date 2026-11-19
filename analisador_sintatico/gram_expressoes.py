'''
A testar 
'''
from ply import yacc
from analisador_lexico.tokens import tokens
from arvore_sintatica.ast_expressoes import (
    OpBinario,
    OpUnario,
    Numero,
    Booleano,
    Id,
    Chamada,
)

s_inicial = "expr"

##############################################################
# Expressões lógicas OU

def p_exprOR(p):
    "exprOr : exprOr OR exprAnd"
    p[0] = OpBinario(
        linha=p.lineno(2),
        operador ="||",
        esquerda=p[1],
        direita=p[3]
    )

def p_exprOr_exprAnd(p):
    "exprOr : exprAnd"
    p[0] = p[1]

##############################################################
# Expressões lógicas E

def p_exprAnd(p):
    "exprAnd : exprAnd AND expr_igual"
    p[0] = OpBinario(
        linha=p.lineno(p),
        operador="&&",
        esquerda=p[1],
        direita=p[3]
    )

def p_exprAnd_expr_igualdade(p):
    "exprAnd : expr_igualdade"
    p[0] = p[1]

##############################################################
# Expressões de igualdade e diferença

def p_expr_igualdade_igual(p):
    "expr_igualdade : expr_igualdade IGUAL expr_relacional"
    p[0] = OpBinario(
        linha=p.lineno(2),
        operador="!=",
        esquerda=p[1],
        direita=p[3]
    )

def p_expr_igualdade_diferente(p):
    "expr_igualdade :  expr_igualdade DIFERENTE expr_relacional"
    p[0] = OpBinario(
        linha=p(2),
        operador="!=",
        esquerda=p[1],
        direita=p[3]
    )

def p_expr_igualdade_relacional(p):
    "expr_igualdade : expr_relacional"
    p[0] - p[3]

##############################################################
# Expressões relacionais
# Apenas um operador, portanto a < b < c tem que produzir erro

def p_expr_relacional(p):
    """expr_relacional : expr_aditiva MENOR expr_aditiva
                       | expr_aditiva MENOR_IGUAL expr_aditiva
                       | expr_aditiva MAIOR expr_aditiva
                       | expr_aditiva MAIOR_IGUAL expr_aditiva"""
    operadores = {
        "MENOR": "<",
        "MENOR_IGUAL": "<=",
        "MAIOR": ">",
        "MAIOR_IGUAL": ">="
    }
    p[0] = OpBinario(
        linha=p.lineno(2),
        operador=operadores[p.slice[2].type],
        esquerda=p[1],
        direita=p[3]
    )

def p_expr_relacional_aditiva(p):
    "expr_relacional : expr_aditiva"
    p[0] = p[1]

##############################################################
# Expressões de mais e menos

def p_expr_aditiva(p):
    """expr_aditiva : expr_aditiva MAIS expr_multiplicativa
                    | expr_aditiva MENOS expr_multiplicativa"""
    operadores = {
        "MAIS": "+",
        "MENOS": "-",
    }
    p[0] = OpBinario(
        linha=p.lineno(2),
        operador=operadores[p.slice[2].type],
        esquerda=p[1],
        direita=p[3]
    )

def p_expr_aditiva_multiplicativa(p):
    p[0] = p[1]


##############################################################
# Expressões de multiplicação e divisão

def p_expr_multiplicativa(p):
    """expr_multiplicativa : expr_multiplicativa ASTERISCO expr_unaria
                        | expr_multiplicativa DIV expr_unaria"""
    operadores = {
        "ASTERISCO": "*",
        "DIV": "/",
    }
    p[0] = OpBinario(
        linha=p.lineno(2),
        operador=operadores[p.slice[2].type],
        esquerda=p[1],
        direita=p[3]
    )

def p_expr_multiplicativa_expr_unaria(p):
    "expr_multiplicativa : expr_unaria"
    p[0] = p[1]

##############################################################
# Expressões unárias
# Recursão à direita permite encadear operadores

def p_expr_unaria_menos(p):
    "expr_unaria : MENOS expr_unaria"
    p[0] = OpUnario(
        linha=p.lineno(1),
        operador="-",
        operando=p[2]
    )

def p_expr_unaria_not(p):
    "expr_unaria : NOT expr_unaria"
    p[0] = OpUnario(
        linha=p.lineno(1),
        operador="!",
        operando=[2]
    )

def p_expr_unaria_expr_primaria(p):
    "expr_unaria : expr_primaria"
    p[0] = p[1]

##############################################################
# Expressões primárias
# Parênteses apenas agrupam a expressão

def p_expr_primaria_numero(p):
    "expr_primaria : NUM"
    p[0] = Numero(linha=p.lineno(1), valor=p[1])

def p_expr_primaria_true(p):
    "expr_primaria : TRUE"
    p[0] = Booleano(linha=p.lineno(1), valor=True)

def p_expr_primaria_false(p):
    "expr_primaria : FALSE"
    p[0] = Booleano(linha=p.lineno(1), valor=False)

def p_expr_primaria_id(p):
    "expr_primaria : IDENT"
    p[0] = Id(linha=p.lineno(1), nome=p[1])

def p_expr_primaria_chamada(p):
    "expr_primaria : chamada"
    p[0] = p[1]

def p_expr_primaria_parenteses(p):
    "expr_primaria : ABRE_PAREN expr FECHA_PAREN"
    p[0] = p[2]

##############################################################
# Chamadas de função e lista de argumentos
# Lista python comum, não uma cadeia de nós da AST

def p_chamada_sem_argumentos(p):
    "chamada : IDENT ABRE_PAREN FECHA_PAREN"
    p[0] = Chamada(
        linha=p.lineno(1),
        nome=p[1],
        argumentos=[]
    )

def p_chamada_com_argumentos(p):
    "chamada : IDENT ABRE_PAREN lista_argumentos FECHA_PAREN"
    p[0] = Chamada(
        linha=p.lineno(1),
        nome=p[1],
        argumentos=[3]
    )

def p_lista_argumentos_um(p):
    "lista_argumentos : expressao"
    p[0] = [p[1]]

def p_lista_argumentos_varios(p):
    "lista_argumentos : lista_argumentos VIRGULA expr"
    p[0] = p[1] + [p[3]]