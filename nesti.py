''' função do arquivo 

    Este é o ponto de partida do compilador, onde é recebido o arquivo ".nesti" pela linha de comando,
    chama as fases da compilação e imprime o que for necessario, (MEPA ou erros), é impostante lembrar que
    este arquivo não realiza papel  da compilação em si

    Entrada: python3 nesti.py <nome do arquivo>.nesti
    Saída: código MEPA na saída padrão, ou lista de erros 
'''

# Importações


'''
    Importar sys da biblioteca padrão do python para:

    sys.argv -> listar o que foi digitado no terminal
    sys.stderr -> faz as mensagens da saída de erro
    sys.exit() -> encerrar o programa
    sys.stdin ->  Lê todas as linhas enviadas pela entrada padrão até o fim do arquivo
    sys.stdout ->  o canal de comunicação por onde o programa envia as informações e 
                   resultados normais de execução, exibindo-os por padrão no console ou terminal
'''

import sys

'''
    Módulos do próprio compilador para fazer as chamadas, no caso do parser e do scanner, eu só chamo uma parte,
    uma vez que o resto não é necessário
'''

import erros #guarda e imprime os erros

from analisador_semantico import semantico #despachante(ligação entre compilador.py e a área semântica) da análise semantica

from mepa import gerador #despachante(ligação entre compilador.py e a área de geração de código) do codigo mepa

from analisador_sintatico.parser import parser # "parser" é o objeto criado com yacc.yacc() dentro de parser.py

from analisador_lexico.scanner import scanner # "scanner" é o objeto criado com lex.lex() dentro de scanner.py 

# Função principal

def main(entrada):
    """
        Essa é a função que executa cada uma das passadas, ele funciona da seguinte maneira, chama uma passada
        verifica se houve erro e se não houve continua a execução até a próxima passada, se houve, encerra o programa

        As entradas e saídas de cada fase são:
            texto -> raiz da AST -> raiz anotada -> código MEPA
    """
    #variaveis

    codigo = le_entrada() #le  o programa nesti e retorna todo o texto do programa

    #passada 1 análise lexica + sintatica
    """
        Aqui parser está rodando, e o scanner está trabalhando junto
        - o parser pede o PRÓXIMO token ao scanner sempre que precisa;
        - o scanner lê o texto até formar um token e devolve
            (tipo, valor, linha); caracteres inválidos são registrados em erros
            (no t_error) e pulados;
        - quando o parser reconhece uma regra da gramática, executa a ação
            dela, que CRIA um nó da AST;
        - no fim, devolve o nó Programa (a raiz da árvore).
        Erros léxicos e sintáticos ficam registrados no módulo erros durante
        esta chamada, por isso há uma unica verificação porteiro depois de tudo.
    """
    raiz = parser.parse(codigo, lexer = scanner)
    verifica_erros()

    if raiz is None:   # o parser não montou a árvore e não registrou erro
        print("ERRO SINTÁTICO: não foi possível montar a árvore do programa", file=sys.stderr)
        return 1

    #passada 2 análise semântica
    """
        O visitador visita a árvore a partir da raiz e isntala a busca de nomes na tabela de símbolos, conferindo
        tipos e anotando na própria árvore(tipo, símbolo, nivel, deslocamento e rótulo)
        não há atribuição de variáveis, pois a função não devolve nada
    """
    semantico.analisa(raiz)
    verifica_erros()

    #passada 3 construção de código MEPA
    """
        Percorre a árvore, agora anotada e devolve o texto em programa MEPA, não há verificação de erros, pois eles
        devem ser identificados até o fim da análise semântica
    """
    codigo_mepa = gerador.gera(raiz)

    #saída -> printa o resultado
    print(codigo_mepa)

    return 0 #sucesso!!!

#Funções auxiliares


def verifica_erros():
    """
        Essa função é executada após o fim da execução de cada etapa e, se houver, imprime os erros e
        interrompe a execução do programa, se não houver, apenas segue em frente
    """
    if erros.tem_erro(): #chama o arquivo de erros e verifica se ele foi chamado
        erros.imprime_tudo() #imprime todos os erros
        sys.exit(1) # significa que a compilação falhou e encerra o programa
    """
        Se o if não é iniciado a execução continua normalmente
    """
    
def le_entrada():
    """
        Essa função confere a linha de comando e devolte o caminho do arquivo de entrada
        Se o usuário usa a entrada errado, é printada a formatação correta
    """
    USO_CORRETO = ("AVISO, você utilizou a formatação errada, utilize o seguinte formato:\n"
    "    python3 nesti.py <nome do arquivo>.nesti")

    '''
        isatty() é True quando NINGUÉM usou o "<", ou seja foi usada a formatação errada
    '''
    if  sys.stdin.isatty():
        print(USO_CORRETO, file=sys.stderr) #além disso envia uma mensagem de erros
        sys.exit(1) #encerra a execução do progama

    return sys.stdin.read() 



#Ponto de entrada

"""
    __name__ vale "__main__" SOMENTE no arquivo que foi executado no terminal.
    Se outro arquivo fizer "import compilador", este bloco não roda.
    Ou seja: as funções acima são o que o arquivo OFERECE; este bloco é o que
    ele FAZ quando é executado.
"""

if __name__ == "__main__":
    """
        No Windows, o terminal nem sempre usa UTF-8. Sem estas duas linhas,
        imprimir uma mensagem com acento pode derrubar o programa com
        UnicodeEncodeError.
    """
    sys.stdin.reconfigure(encoding="utf-8-sig", errors="replace")
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

    """
        sys.argv[1:] tira o nome do próprio script da lista.
        O valor devolvido por principal (0) vira o código de saída do programa.
    """
    sys.exit(main(sys.argv[1:]))

