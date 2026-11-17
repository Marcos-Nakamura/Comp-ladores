import ply.lex as lex
from tokens import tokens, reservadas

t_ABRE_PAREN    = r'\()'
t_FECHA_PAREN   = r'\)'
t_PONT_VIRG     = r';'
t_ABRE_CHAVE    = r'\{'
t_FECHA_CHAVE   = r'\}'
t_VIRGULA       = r','
t_SETA          = r'->'
t_ATRIB         = r'='
t_IGUAL         = r'=='
t_DIFERENTE     = r'!='
t_MENOR         = r'<'
t_MENOR_IGUAL   = r'<='
t_MAIOR         = r'>'
t_MAIOR_IGUAL   = r'>='
t_MAIS          = r'\+'
t_MENOS         = r'-'
t_ASTERISCO     = r'\*'
t_DIV           = r'/'
t_AND           = r'&&'
t_OR            = r'\|\|'
t_NOT           = r'!'

def t_IDENT(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reservadas.get(t.value, 'IDENT')
    return t

# Números
def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Ignorar espaços e tabulações
t_ignore = ' \t'