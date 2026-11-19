'''
Erro -> tipo especial usado internamente pela análise semântica para indicar
que uma expressão apresentou algum problema
'''
ERRO = "erro"
INT = "int"
BOOL = "bool"

def tipo_resultado(operador, tipo_esquerdo, tipo_direito=None):
    '''
    Função que será integrado com a análise semântica (sem_expressoes)
    '''
    # Propagação de erro: evita diagnósticos em cascata.
    if tipo_esquerdo == ERRO or tipo_direito == ERRO:
        return ERRO

    # Operadores unários.
    if tipo_direito is None:
        if operador == "-" and tipo_esquerdo == INT:
            return INT
        if operador == "!" and tipo_esquerdo == BOOL:
            return BOOL
        return ERRO

    # Operadores aritméticos.
    if operador in {"+", "-", "*", "/"}:
        return INT if tipo_esquerdo == INT and tipo_direito == INT else ERRO

    # Operadores relacionais.
    if operador in {"<", "<=", ">", ">="}:
        return BOOL if tipo_esquerdo == INT and tipo_direito == INT else ERRO 

    # Igualdade e diferença
    if operador in {"==", "!="}:
        if tipo_esquerdo in {INT, BOOL} and tipo_esquerdo == tipo_direito:
            return BOOL
        return ERRO

    # Operadores lógicos
    if operador in {"&&", "||"}:
        return BOOL if tipo_esquerdo == BOOL and tipo_direito == BOOL else ERRO

    return ERRO