from arvore_sintatica.ast_expressoes import *

# b * 2
multiplicacao = OpBinario(
    linha=1,
    operador="*",
    esquerda=Id(linha=1, nome="b"),
    direita=Numero(linha=1, valor=2)
)

# a + (b * 2)
arvore = OpBinario(
    linha=1,
    operador="+",
    esquerda=Id(linha=1, nome="a"),
    direita=multiplicacao
)

print(arvore)