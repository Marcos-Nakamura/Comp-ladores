"Executa os casos Nesti pelo compilador e pelo interpretador MEPA 5.0."
import os
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory

TESTES = Path(__file__).resolve().parent
RAIZ = TESTES.parent

def executar(argumentos, entrada=""):
    return subprocess.run(
        [sys.executable, "-B", *argumentos], input=entrada, text=True,
        encoding="utf-8", capture_output=True, cwd=RAIZ, timeout=20,
        env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONDONTWRITEBYTECODE": "1"},
    )

def anotacoes(fonte, chave):
    prefixo = f"// {chave}:"
    return [linha.removeprefix(prefixo).strip() for linha in fonte.splitlines()
            if linha.startswith(prefixo)]

def conferir(nome, recebido, esperado):
    if recebido != esperado:
        raise ValueError(f"{nome}\n    esperado: {esperado!r}\n    recebido: {recebido!r}")

def verificar(caso, pasta):
    fonte = caso.read_text(encoding="utf-8")
    compilacao = executar(["nesti.py"], fonte)
    if caso.parent.name == "erros":
        esperados = anotacoes(fonte, "erro")
        if not esperados:
            raise ValueError("falta a anotação // erro:")
        mensagens = [linha for linha in compilacao.stderr.splitlines()
                     if linha != "Generating LALR tables"]
        conferir("diagnósticos", mensagens, esperados)
        conferir("código de saída do compilador", compilacao.returncode, 1)
        conferir("código MEPA emitido", compilacao.stdout, "")
        return

    if compilacao.returncode:
        raise ValueError(compilacao.stderr.strip())
    instrucoes = compilacao.stdout.splitlines()
    conferir("fim do programa", instrucoes[-2:], ["PARA", "FIM"])
    for instrucao in anotacoes(fonte, "instrucao"):
        if instrucao not in instrucoes:
            raise ValueError(f"instrução esperada ausente: {instrucao}")

    programa = pasta / (caso.stem + ".mepa")
    programa.write_text(compilacao.stdout, encoding="utf-8")
    entrada = "\n".join(anotacoes(fonte, "entrada")) + "\n"
    resultado = executar(["mepa/mepa_pt.py", "--silent", "--progfile", str(programa)], entrada)
    if resultado.returncode or not re.fullmatch(r"\d+ instruções executadas", resultado.stderr.strip()):
        raise ValueError(f"erro da MEPA: {resultado.stderr.strip()}")
    saidas = anotacoes(fonte, "saida")
    if not saidas:
        raise ValueError("falta a anotação // saida:")
    esperado = "".join(valor + "\n" for valor in " ".join(saidas).split())
    conferir("saída da execução", resultado.stdout, esperado)

def main():
    falhas = total = 0
    with TemporaryDirectory() as temp:
        for grupo in ("validos", "erros"):
            casos = sorted((TESTES / grupo).glob("*.nesti"))
            if not casos:
                print(f"FALHOU {grupo}: nenhum caso encontrado")
                return 1
            for caso in casos:
                total += 1
                nome = caso.relative_to(TESTES)
                try:
                    verificar(caso, Path(temp))
                except (ValueError, OSError, subprocess.TimeoutExpired) as erro:
                    falhas += 1
                    print(f"FALHOU {nome}\n    {erro}")
                else:
                    print(f"PASSOU {nome}")

    print(f"\n{total - falhas}/{total} passaram; {falhas} falharam.")
    return int(bool(falhas))


if __name__ == "__main__":
    sys.exit(main())