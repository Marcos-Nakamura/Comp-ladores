'''
Análise semântica de expressões da linguagem Nesti.

O Contexto deve oferecer:
  - visitar(no)
  - tabela.buscar(nome)
  - erro(linha, mensagem)

As expressões recebem as anotações 'tipo'; Id e Chamada também
recebem 'simbolo'. Chamadas void são proibidas como expressões, mas
permitidas como comandos isolados por analisar_chamada_como_comando().
'''
from __future__ import annotations
from .tipos_regras import tipo_resultado, ERRO, INT, BOOL

VOID = "void"

def linha(no):
    return getattr(no, "linha", None)

def categoria(simbolo):
    categoria = getattr(simbolo, "categoria", "")
    return categoria.strip().lower().replace("á", "a").replace("â", "a")

def eh_funcao(simbolo):
    return categoria(simbolo) in {"funcao", "function"}

def eh_variavel_ou_parametro(simbolo):
    return categoria(simbolo) in {
        "variavel", "parametro", "variable", "parameter"
    }

def tipo_ou_erro(tipo):
    # tipos desconhecidos devem ser convertidos para ERRO
    return tipo if tipo in {INT, BOOL, ERRO, VOID} else ERRO

def visita_Numero(no, contexto):
    no.tipo = INT
    return no.tipo

def visita_Booleano(no, contexto):
    no.tipo = BOOL
    return no.tipo

def visita_Variavel(no, contexto):
    simbolo = contexto.tabela.buscar(no.nome)
    no.simbolo = simbolo

    if simbolo is None:
        contexto.erro(linha(no), f"identificador '{no.nome}' não declarado")
        no.tipo = ERRO
        return no.tipo

    if eh_funcao(simbolo):
        contexto.erro(linha(no), f"'{no.nome}' é uma função, não é variável")
        no.tipo = ERRO
        return no.tipo

    if not eh_variavel_ou_parametro(simbolo):
        contexto.erro(linha(no), f"'{no.nome}' não é uma variável")
        no.tipo = ERRO
        return no.tipo

    no.tipo = tipo_ou_erro(getattr(simbolo, "tipo", None))
    if no.tipo == ERRO:
        contexto.erro(
            linha(no),
            f"não foi possível determinar o tipo da variável '{no.nome}'"
        )
    
    return no.tipo

def visita_OpBinario(no, contexto):
    tipo_esquerdo = tipo_ou_erro(contexto.visitar(no.esquerda))
    tipo_direito = tipo_ou_erro(contexto.visitar(no.direita))

    resultado = tipo_resultado(
        no.operador, tipo_esquerdo, tipo_direito
    )

    if resultado == ERRO and tipo_esquerdo != ERRO and tipo_direito != ERRO:
        contexto.erro(
            linha(no),
            f"operandos incompatíveis com o operador '{no.operador}': "
            f"'{tipo_esquerdo}' e '{tipo_direito}'"
        )

    no.tipo = resultado
    return no.tipo

def visita_OpUnario(no, contexto):
    tipo_operando = tipo_ou_erro(contexto.visitar(no.operando))
    resultado = tipo_resultado(no.operador, tipo_operando)

    if resultado == ERRO and tipo_operando != ERRO:
        contexto.erro(
            linha(no),
            f"operador unário '{no.operador}' incompatível com o tipo "
            f"'{tipo_operando}'"
        )

    no.tipo = resultado
    return no.tipo

def visitar_argumentos(no, contexto):
    tipos = []
    for argumento in no.argumentos:
        tipos.append(tipo_ou_erro(contexto.visitar(argumento)))
    return tipos

def analisar_chamada(no, contexto, exigir_valor):
    # A busca considera o escopo mais interno primeiro. Assim, uma variável
    # que sombreia uma função será encontrada e corretamente rejeitada.
    simbolo = contexto.tabela.buscar(no.nome)
    no.simbolo = simbolo

    # Visita todos os argumentos mesmo se o nome chamado estiver incorreto.
    tipos_argumentos = visitar_argumentos(no, contexto)

    if simbolo is None:
        contexto.erro(linha(no), f"função '{no.nome}' não declarada")
        no.tipo = ERRO
        return no.tipo

    if not eh_funcao(simbolo):
        contexto.erro(linha(no), f"'{no.nome}' não é uma função")
        no.tipo = ERRO
        return no.tipo

    tipos_parametros = getattr(simbolo, "tipos_parametros", None) or []

    if len(tipos_argumentos) != len(tipos_parametros):
        contexto.erro(
            linha(no),
            f"função '{no.nome}' espera {len(tipos_parametros)} argumento(s), "
            f"mas recebeu {len(tipos_argumentos)}"
        )

    # A comparação é posicional: argumento 1 com parâmetro 1, e assim por diante.
    for indice, (tipo_arg, tipo_param) in enumerate(
        zip(tipos_argumentos, tipos_parametros), start=1
    ):
        if tipo_arg != ERRO and tipo_arg != tipo_param:
            contexto.erro(
                linha(no.argumentos[indice - 1]),
                f"tipo do argumento {indice} da função '{no.nome}' "
                f"é '{tipo_arg}', mas o parâmetro espera '{tipo_param}'"
            )

    tipo_retorno = tipo_ou_erro(getattr(simbolo, "tipo", None))

    if tipo_retorno == ERRO:
        contexto.erro(
            linha(no),
            f"tipo de retorno da função '{no.nome}' inválido ou desconhecido"
        )
        no.tipo = ERRO
        return no.tipo

    if exigir_valor and tipo_retorno == VOID:
        contexto.erro(
            linha(no),
            f"função '{no.nome}' não retorna valor e não pode ser usada "
            f"em uma expressão"
        )
        no.tipo = ERRO
        return no.tipo

    no.tipo = tipo_retorno
    return no.tipo

def visita_Chamada(no, contexto):
    """Visita uma chamada usada como expressão; void é erro."""
    return analisar_chamada(no, contexto, exigir_valor=True)


def analisar_chamada_como_comando(no, contexto):
    """
    Use em sem_comandos.py para uma chamada usada como comando isolado.
    Verifica função e argumentos, mas permite retorno void.
    """
    return analisar_chamada(no, contexto, exigir_valor=False)