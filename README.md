# Compilador da linguagem Nesti

## Visão geral

O projeto consiste no desenvolvimento de um compilador para a linguagem
experimental **Nesti**, utilizando **Python** e a ferramenta **PLY**
para geração do analisador léxico e do parser. O compilador recebe um
arquivo-fonte Nesti pela linha de comando, realiza as análises léxica,
sintática e semântica, constrói uma Árvore Sintática Abstrata (AST) e
gera código para a máquina **MEPA**.

## Principais funcionalidades

### 1. Análise léxica

-   Reconhece palavras reservadas, identificadores, números inteiros,
    operadores e símbolos especiais da linguagem.
-   Ignora espaços em branco, tabulações, quebras de linha e comentários
    de linha iniciados por `//`.
-   Contabiliza as linhas do código para indicar a localização de erros
    léxicos.
-   Identifica caracteres ou sequências inválidas e emite mensagens de
    erro.

### 2. Análise sintática e construção da AST

-   Verifica se o código-fonte segue a gramática da linguagem Nesti.
-   Reconhece declarações de variáveis e funções, parâmetros, comandos e
    expressões.
-   Suporta estruturas condicionais `if/else`, repetição `while`,
    atribuições, retornos, chamadas de função e operações de entrada e
    saída.
-   Constrói uma AST que representa as construções relevantes do
    programa, sem elementos sintáticos desnecessários, como
    delimitadores e ponto e vírgula.
-   Utiliza a AST como representação intermediária para as etapas
    semântica e de geração de código.

### 3. Análise semântica

-   Mantém uma tabela de símbolos com informações sobre identificadores,
    categorias, tipos, escopos e níveis léxicos.
-   Verifica declarações duplicadas no mesmo escopo e impede que uma
    nova declaração substitua a anterior.
-   Verifica a declaração e a visibilidade de variáveis e funções.
-   Implementa escopo léxico, permitindo acesso a identificadores de
    escopos ancestrais e sombreamento entre escopos diferentes.
-   Verifica compatibilidade de tipos em inicializações, atribuições,
    expressões, parâmetros e retornos.
-   Valida chamadas de função, incluindo existência, visibilidade,
    quantidade e tipos dos argumentos.
-   Verifica as condições de `if` e `while`, que devem produzir valores
    booleanos.
-   Valida os argumentos dos comandos `read` e `print`.
-   Verifica o uso correto de `return` conforme o tipo de retorno da
    função.

### 4. Recursos da linguagem Nesti

-   Tipos primitivos `int` e `bool`, além de `void` como tipo de retorno
    de função.
-   Declaração de variáveis com ou sem inicialização.
-   Definição de funções com parâmetros e possibilidade de aninhamento e
    recursão direta.
-   Estruturas de controle `if/else` e `while`.
-   Entrada de dados com `read` e saída com `print`.
-   Expressões aritméticas (`+`, `-`, `*`, `/`), relacionais (`<`, `<=`,
    `>`, `>=`), de igualdade (`==`, `!=`) e lógicas (`&&`, `||`, `!`).
-   Divisão inteira e valores booleanos `true` e `false`.

### 5. Geração de código MEPA

-   Percorre a AST após as análises para gerar instruções destinadas à
    máquina MEPA.
-   Produz o código MEPA na saída padrão ou permite seu redirecionamento
    para um arquivo.

## Execução

O compilador deve ser executado pela linha de comando, recebendo como
argumento o caminho do arquivo que contém o código-fonte em Nesti. O
código MEPA produzido pode ser exibido no terminal ou redirecionado para
um arquivo.
