'''
Define quais tipos cada operador de Nesti aceita e qual é o tipo do resultado.
O tipo especial ERRO sinaliza uma expressão inválida e evita mensagens de erro em cascata.
'''
ERRO = "erro"
INT = "int"
BOOL = "bool"

SEM_OPERANDO_DIREITO = object()

def tipo_resultado(operador, tipo_esquerdo, tipo_direito=SEM_OPERANDO_DIREITO):
    '''
    Função que será integrado com a análise semântica (sem_expressoes)
    '''
    # Propagação de erro: evita diagnósticos em cascata.
    if tipo_esquerdo == ERRO or tipo_direito == ERRO:
        return ERRO

    # Operadores unários.
    if tipo_direito is SEM_OPERANDO_DIREITO:
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