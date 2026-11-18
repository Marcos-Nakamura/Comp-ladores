import ply.lex as lex
from .tokens import tokens, p_reservadas
import erros

t_ABRE_PAREN    = r'\('
t_FECHA_PAREN   = r'\)'
t_PONTO_VIRG     = r';'
t_ABRE_CHAVE    = r'\{'
t_FECHA_CHAVE   = r'\}'
t_VIRGULA       = r','
t_SETA          = r'->'
t_IGUAL         = r'=='
t_DIFERENTE     = r'!='
t_MENOR_IGUAL   = r'<='
t_MAIOR_IGUAL   = r'>='
t_MENOR         = r'<'
t_MAIOR         = r'>'
t_ATRIB         = r'='
t_MAIS          = r'\+'
t_MENOS         = r'-'
t_ASTERISCO     = r'\*'
t_DIV           = r'/'
t_AND           = r'&&'
t_OR            = r'\|\|'
t_NOT           = r'!'

# Ignora uma linha inteira após //
def t_COMENTARIO(t):
    r'//[^\n]*'
    pass

# Descarta por completo números inválidos (1abc)
def t_NUM_INVALIDO(t):
    r'\d+[a-zA-Z_][a-zA-Z0-9_]*'
    erros.registra(
        fase="LÉXICO",
        linha=t.lexer.lineno,
        mensagem=f"Identificador inválido '{t.value}' (não pode iniciar com número)"
    )

def t_NUM(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_IDENT(t):
    r'[a-zA-Z][a-zA-Z0-9_]*'
    t.type = p_reservadas.get(t.value, 'IDENT')
    return t

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Ignorar espaços e tabulações
t_ignore = ' \t\r'

def t_error(t):
    caractere_invalido = t.value[0]
    erros.registra(
        fase="LÉXICO",
        linha=t.lexer.lineno,
        mensagem=f"Caractere inválido '{caractere_invalido}'"
    )
    t.lexer.skip(1)

scanner = lex.lex()