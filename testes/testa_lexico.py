from sys import stdin
from analisador_lexico.scanner import scanner

data = stdin.read()
scanner.input(data)
while True:
    tok = scanner.token()
    if not tok:
        break
print(tok)