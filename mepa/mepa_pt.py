"""Ponto de entrada para o interpretador MEPA 5.0 distribuído em m_mepa."""

from pathlib import Path
import runpy
import sys


if __name__ == "__main__":
    raiz = Path(__file__).resolve().parents[1]
    distribuicao = raiz / "m_mepa"
    sys.path[:0] = [str(distribuicao), str(raiz)]
    runpy.run_path(str(distribuicao / "mepa_pt.py"), run_name="__main__")
