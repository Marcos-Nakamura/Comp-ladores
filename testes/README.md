# Testes do compilador Nesti

Na raiz do projeto, execute:

```sh
python3 testes/rodar.py
```

O roteiro imprime PASSOU ou FALHOU para cada programa `.nesti` de `validos/` e `erros/`. Em caso de falha, mostra o diagnóstico ou a diferença entre o resultado esperado e o recebido. O código de saída é 0 quando todos passam e 1 quando há falhas.

## Programas e expectativas

- Em `validos/`, cada programa traz a saída de execução em `// saida:`. Cada número corresponde a uma linha impressa. O caso de leitura inclui os dados de entrada em `// entrada:`.
- Em `erros/`, cada programa traz o diagnóstico completo em `// erro:`, com fase, linha e mensagem. Os nomes de `sem01` a `sem18` seguem a numeração do checklist semântico. O roteiro também exige que o compilador termine com erro e deixe vazia a saída de código MEPA.
- O roteiro exige `PARA` e `FIM` no final de todo programa válido. Em `identidade.nesti`, as anotações `// instrucao:` conferem a leitura do parâmetro em −5 e a gravação do retorno em −6. Em `subtracao.nesti`, o resultado 7 verifica a ordem dos argumentos.

Para acrescentar um caso, coloque um arquivo `.nesti` na pasta correspondente e anote as expectativas no fim, com os comentários iniciando na primeira coluna.

O ponto de entrada em `mepa/mepa_pt.py` usa o interpretador 5.0 distribuído na pasta `m_mepa/`. 