from sys import stdin
from analisador_lexico.scanner import scanner
import erros # ajuste o import conforme a pasta onde erros.py está

data = stdin.read()
scanner.input(data)

while True:
    tok = scanner.token()
    if not tok:
        break
    print(tok)

if erros.tem_erro():
    erros.imprime_tudo()