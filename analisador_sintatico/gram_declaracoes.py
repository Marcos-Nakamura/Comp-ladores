"""
Escrever as regras de programa, funções aninhadas, parâmetros, variáveis e tipos.

Entrada: tokens, expressões e comandos
Saída: Programa (raiz) e demais declarações
Depende de: ast_declaracoes.py 


"""

from arvore_sintatica.ast_declaracoes import Programa, DeclFuncao, Parametro, DeclVar



#-----------------------PROGRAMA---------------------------#

# p_programa
# Pode: o programa inteiro, com as três partes possivelmente vazias.

def p_programa(p):
    """
    programa : PROGRAM IDENT ABRE_CHAVE declaracoes_variaveis declaracoes_funcoes comandos FECHA_CHAVE
    """
    p[0] = Programa(nome=p[2], variaveis=p[4], funcoes=p[5], comandos=p[6], 
                    linha=p.lineno(1))




#-----------------------VARIÁVEIS--------------------------#

# p_declaracoes_variaveis
# Pode: zero ou mais declarações seguidas.
# (sempre devolver lista Python, nunca None)

def p_declaracoes_variaveis(p):
    """
    declaracoes_variaveis : declaracoes_variaveis declaracao_variavel
                          | empty
    """
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []


# p_declaracao_variavel
# Pode: com ou sem inicialização.
# Não pode: tipo void

def p_declaracao_variavel(p):
    """
    declaracao_variavel : tipo IDENT PONTO_VIRG
                       | tipo IDENT ATRIB expressao PONTO_VIRG
    """
    if len(p) == 6:
        p[0] = DeclVar(tipo=p[1], nome=p[2], inicializacao=p[4], linha=p.lineno(2))
    else:
        p[0] = DeclVar(tipo=p[1], nome=p[2], linha=p.lineno(2))





#-----------------------FUNÇÕES-------------------------#

# p_declaracoes_funcoes
# Pode: zero ou mais funções seguidas.

def p_declaracoes_funcoes(p):
    """
    declaracoes_funcoes : declaracoes_funcoes declaracao_funcao
                        | empty
    """
    if len(p) == 3:
        p[0] = p[1] + [p[2]]
    else:
        p[0] = []


# p_declaracao_funcao

def p_declaracao_funcao(p):
    """
    declaracao_funcao : FUN IDENT ABRE_PAREN parametros_opcionais FECHA_PAREN SETA tipo_retorno ABRE_CHAVE declaracoes_variaveis declaracoes_funcoes comandos FECHA_CHAVE
    """
    p[0] = DeclFuncao(nome=p[2], parametros=p[4], tipo_retorno=p[7],
                      variaveis=p[9], funcoes=p[10], comandos=p[11], 
                      linha=p.lineno(1))



#----------------------PARAMETROS------------------------#

# p_parametros_opcionais
# Pode: nenhum parâmetro, ou uma lista

def p_parametros_opcionais(p):
    """
    parametros_opcionais : lista_parametros
                        | empty
    """
    if p.slice[1].type == "empty":
        p[0] = []
    else:
        p[0] = p[1]


# p_lista_parametros
# Pode: um ou mais parâmetros separados por vírgula.

def p_lista_parametros(p):
    """
    lista_parametros : lista_parametros VIRGULA parametro
                     | parametro
    """
    if len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = [p[1]]


# p_parametro
# Pode: int ou bool.

def p_parametro(p):
    """
    parametro : tipo IDENT
    """
    p[0] = Parametro(tipo=p[1], nome=p[2], 
                     linha=p.lineno(2))


#-------------------------TIPOS--------------------------#

# p_tipo
# Pode: INT ou BOOL.

def p_tipo(p):
    """
    tipo : INT
         | BOOL
    """
    p[0] = p[1]


# p_tipo_retorno
# Pode: int, bool ou void.

def p_tipo_retorno(p):
    """
    tipo_retorno : tipo
                 | VOID
    """
    p[0] = p[1]
