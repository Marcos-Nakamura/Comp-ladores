"""Gera instruções MEPA para os nós de expressão anotados pela semântica."""

BINARIOS = {
    "+": "SOMA", "-": "SUBT", "*": "MULT", "/": "DIVI",
    "&&": "CONJ", "||": "DISJ",
    "<": "CMME", ">": "CMMA", "==": "CMIG", "!=": "CMDG",
    "<=": "CMEG", ">=": "CMAG",
}
UNARIOS = {"-": "INVR", "!": "NEGA"}

def visita_Numero(no, contexto):
    contexto.emissor.emite("CRCT", no.valor)

def visita_Booleano(no, contexto):
    contexto.emissor.emite("CRCT", int(no.valor))

def visita_Id(no, contexto):
    simbolo = no.simbolo
    contexto.emissor.emite("CRVL", simbolo.nivel, simbolo.deslocamento)

def visita_OpBinario(no, contexto):
    contexto.visitar(no.esquerda)
    contexto.visitar(no.direita)
    contexto.emissor.emite(BINARIOS[no.operador])

def visita_OpUnario(no, contexto):
    contexto.visitar(no.operando)
    contexto.emissor.emite(UNARIOS[no.operador])

def visita_Chamada(no, contexto):
    if no.tipo != "void":
        contexto.emissor.emite("AMEM", 1)
    # S17 atribui o deslocamento -5 ao último parâmetro empilhado.
    for argumento in no.argumentos:
        contexto.visitar(argumento)
    chamador = contexto.funcao_atual
    nivel_chamador = chamador.simbolo.nivel if chamador is not None else 0
    contexto.emissor.emite("CHPR", no.simbolo.rotulo, nivel_chamador)