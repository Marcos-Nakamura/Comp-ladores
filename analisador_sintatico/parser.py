"""
Monta o parser a partir das três gramáticas, trata erros sintáticos e entrega a raiz da AST.

Entrada: tokens
Saída: raiz da AST (nó Programa) ou erro sintático (registrado em erros.py)
Depende de: gram_expressoes.py, gram_comandos.py, gram_declaracoes.py, tokens.py, erros.py

"""

from ply import yacc
from analisador_sintatico.gram_comandos import *
from analisador_sintatico.gram_declaracoes import *
from analisador_sintatico.gram_expressoes import *
from analisador_lexico.tokens import tokens
import erros


#-------------Símbolo inicial--------------#


start = "programa"


#---------------Regra vazia-----------------#


def p_empty(p):
  """
  empty :
  """
  pass


#--------------Erro sintático---------------#


def p_error(p):

  houve_lexico = any(e.fase == "LÉXICO" for e in erros.lista_erros)

  if not houve_lexico:
    if p:
        erros.registra("SINTÁTICO", p.lineno, f"token inesperado '{p.value}'")
    else:
        erros.registra("SINTÁTICO", None, "fim inesperado do arquivo")

  # descartar tokens até EOF
  while True:
    tok = parser.token()    # pedir próximo token
    if not tok:             # se veio None, acabou
        break


#--------------Construção do parser--------------#


parser = yacc.yacc(debug=True, write_tables=True)


#------------------------------------------------#