"""
Verificar e instalar todas as declarações (programa, variáveis, funções e
parâmetros), controlando escopos, níveis, deslocamentos e rótulos, e anotar
na AST tudo o que a geração vai precisar.

Entrada: nós de declaração (Programa, DeclVar, DeclFuncao) + contexto
Saída: símbolos instalados, anotações na AST, erros registrados (erros.py)

"""

from __future__ import annotations
from analisador_semantico.tabela_simbolos import Simbolo
from analisador_semantico.tipos_regras import BOOL, INT, ERRO



PROGRAMA, VARIAVEL, PARAMETRO, FUNCAO = "programa", "variavel", "parametro", "funcao"
EXIGE_RETORNO = {INT, BOOL}



def visita_Programa(no, ctx):
    s = Simbolo(nome=no.nome, categoria=PROGRAMA, nivel=ctx.tabela.nivel)
    ctx.tabela.instalar(s)
    no.simbolo = s
    _visita_bloco(no, ctx)



def visita_DeclVar(no, ctx):
    if no.inicializacao is not None:
        t = ctx.visitar(no.inicializacao)
        if t != ERRO and t != no.tipo:
            ctx.erro(no.linha, f"variável '{no.nome}' declarada como {no.tipo} mas inicializada com {t}")
    s = Simbolo(nome=no.nome, categoria=VARIAVEL, nivel=ctx.tabela.nivel, tipo=no.tipo)
    if ctx.tabela.instalar(s):
        s.deslocamento = ctx.tabela.prox_deslocamento()
    else:
        ctx.erro(no.linha, f"variável '{no.nome}' já declarada neste escopo")
    no.simbolo = s



def visita_DeclFuncao(no, ctx):
    s = Simbolo(nome=no.nome, categoria=FUNCAO,
                nivel=ctx.tabela.nivel + 1,
                tipo=no.tipo_retorno,
                tipos_parametros=[p.tipo for p in no.parametros],
                rotulo=_novo_rotulo_funcao(ctx))
    if not ctx.tabela.instalar(s):                      # ainda no escopo de FORA → recursão
        ctx.erro(no.linha, f"função '{no.nome}' já declarada neste escopo")
    no.simbolo = s
    anterior = ctx.funcao_atual
    ctx.funcao_atual = no
    no.tem_return = False
    ctx.tabela.entrar()
    try:
        _instala_parametros(no, ctx)
        _visita_bloco(no, ctx)
        if no.tipo_retorno in EXIGE_RETORNO and not no.tem_return:
            ctx.erro(no.linha, f"função '{no.nome}' de tipo {no.tipo_retorno} não retorna valor")
    finally:
        ctx.tabela.sair()
        ctx.funcao_atual = anterior



# (programa e DeclFuncao têm os mesmos campos)

def _visita_bloco(no, ctx):                             
    for v in no.variaveis: ctx.visitar(v)
    for f in no.funcoes:   ctx.visitar(f)
    for c in no.comandos:  ctx.visitar(c)
  


def _novo_rotulo_funcao(ctx):
    ctx.tabela.cont_rotulos += 1
    return f"F{ctx.tabela.cont_rotulos}"

  

def _instala_parametros(no, ctx):
    """
    Pode:     ser chamada logo depois de tabela.entrar(), com a lista completa
              (o deslocamento depende de n).
    Não pode: usar prox_deslocamento() (é das variáveis locais: 0, 1, 2...).
    Quebra:   item 1 (parâmetro repetido) vai para contexto.erro; o repetido
              recebe símbolo no nó, mas não entra na tabela.
    """
    n = len(no.parametros)
    for i, p in enumerate(no.parametros):
        s = Simbolo(nome=p.nome, categoria=PARAMETRO, nivel=ctx.tabela.nivel, tipo=p.tipo,
                    deslocamento=-(4 + n - i))
        if not ctx.tabela.instalar(s):
            ctx.erro(p.linha, f"parâmetro '{p.nome}' já declarado neste escopo")
        p.simbolo = s