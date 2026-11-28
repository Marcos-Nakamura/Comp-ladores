"""
Gerar o código MEPA do programa e das funções aninhadas: memória, entrada e
saída de procedimento, saltos e inicializações.

Entrada: nós de declaração JÁ ANOTADOS pela S17 + contexto da geração
Saída: instruções MEPA no emissor

"""


def _gera_bloco(no, contexto):
    e = contexto.emissor
    for v in no.variaveis:
        contexto.visitar(v)
    pula = e.novo_rotulo()
    e.emite("DSVS", pula)
    for f in no.funcoes:
        contexto.visitar(f)
    e.marca(pula)
    for c in no.comandos:
        contexto.visitar(c)


def visita_Programa(no, contexto):
    e = contexto.emissor
    g = len(no.variaveis)
    e.emite("INPP")
    e.emite("AMEM", g)
    _gera_bloco(no, contexto)
    e.emite("DMEM", g)
    e.emite("PARA")
    e.emite("FIM")


def visita_DeclFuncao(no, contexto):
    e = contexto.emissor
    k = no.simbolo.nivel
    m = len(no.variaveis)
    n = len(no.parametros)
    no.rotulo_fim = e.novo_rotulo()
    anterior = contexto.funcao_atual
    contexto.funcao_atual = no
    try:
        e.marca(no.simbolo.rotulo)
        e.emite("ENPR", k)
        e.emite("AMEM", m)
        _gera_bloco(no, contexto)
        e.marca(no.rotulo_fim)
        e.emite("DMEM", m)
        e.emite("RTPR", n)
    finally:
        contexto.funcao_atual = anterior


def visita_DeclVar(no, contexto):
    if no.inicializacao is None:
        return
    contexto.visitar(no.inicializacao)
    s = no.simbolo
    contexto.emissor.emite("ARMZ", s.nivel, s.deslocamento)