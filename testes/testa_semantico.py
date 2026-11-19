from analisador_semantico.tipos_regras import tipo_resultado, ERRO, INT, BOOL

def testa_tipo_regras():
    """Testa os 14 operadores com tipos válidos, inválidos e erro propagado."""
    casos = [
        # Unários
        ("- unário válido", "-", INT, None, INT),
        ("- unário inválido", "-", BOOL, None, ERRO),
        ("- unário propaga erro", "-", ERRO, None, ERRO),
        ("! unário válido", "!", BOOL, None, BOOL),
        ("! unário inválido", "!", INT, None, ERRO),
        ("! unário propaga erro", "!", ERRO, None, ERRO),

        # Aritméticos binários
        ("+", "+", INT, INT, INT),
        ("+ inválido", "+", BOOL, INT, ERRO),
        ("+ propaga erro", "+", ERRO, INT, ERRO),
        ("- binário", "-", INT, INT, INT),
        ("- binário inválido", "-", INT, BOOL, ERRO),
        ("- binário propaga erro", "-", INT, ERRO, ERRO),
        ("*", "*", INT, INT, INT),
        ("* inválido", "*", BOOL, BOOL, ERRO),
        ("* propaga erro", "*", INT, ERRO, ERRO),
        ("/", "/", INT, INT, INT),
        ("/ inválido", "/", BOOL, INT, ERRO),
        ("/ propaga erro", "/", ERRO, INT, ERRO),

        # Relacionais
        ("<", "<", INT, INT, BOOL),
        ("< inválido", "<", BOOL, INT, ERRO),
        ("< propaga erro", "<", ERRO, INT, ERRO),
        ("<=", "<=", INT, INT, BOOL),
        ("<= inválido", "<=", INT, BOOL, ERRO),
        ("<= propaga erro", "<=", INT, ERRO, ERRO),
        (">", ">", INT, INT, BOOL),
        ("> inválido", ">", BOOL, BOOL, ERRO),
        ("> propaga erro", ">", ERRO, INT, ERRO),
        (">=", ">=", INT, INT, BOOL),
        (">= inválido", ">=", BOOL, INT, ERRO),
        (">= propaga erro", ">=", INT, ERRO, ERRO),

        # Igualdade e diferença
        ("== int", "==", INT, INT, BOOL),
        ("== bool", "==", BOOL, BOOL, BOOL),
        ("== tipos diferentes", "==", INT, BOOL, ERRO),
        ("== propaga erro", "==", ERRO, BOOL, ERRO),
        ("!= int", "!=", INT, INT, BOOL),
        ("!= bool", "!=", BOOL, BOOL, BOOL),
        ("!= tipos diferentes", "!=", INT, BOOL, ERRO),
        ("!= propaga erro", "!=", INT, ERRO, ERRO),

        # Lógicos
        ("&&", "&&", BOOL, BOOL, BOOL),
        ("&& inválido", "&&", INT, BOOL, ERRO),
        ("&& propaga erro", "&&", ERRO, BOOL, ERRO),
        ("||", "||", BOOL, BOOL, BOOL),
        ("|| inválido", "||", BOOL, INT, ERRO),
        ("|| propaga erro", "||", BOOL, ERRO, ERRO),
    ]

    falhas = []
    for descricao, operador, esquerdo, direito, esperado in casos:
        obtido = tipo_resultado(operador, esquerdo, direito)
        status = "OK" if obtido == esperado else "FALHOU"
        print(f"{status:7} | {descricao:24} | esperado={esperado:5} obtido={obtido}")
        if obtido != esperado:
            falhas.append((descricao, esperado, obtido))

    print(f"\n{len(casos) - len(falhas)}/{len(casos)} testes passaram.")
    if falhas:
        raise AssertionError(f"Falhas nos testes: {falhas}")


if __name__ == "__main__":
    testa_tipo_regras()