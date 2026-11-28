"""Ponto de entrada para o interpretador MEPA 5.0 distribuído em m_mepa."""

from pathlib import Path
import runpy
import sys


if __name__ == "__main__":
    raiz = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(raiz))
    # O interpretador seleciona os mnemônicos portugueses pelo nome mepa_pt.py.
    runpy.run_module("m_mepa.mepa", run_name="__main__")
