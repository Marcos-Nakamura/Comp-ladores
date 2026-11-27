"""
    Este arquivo funciona como despachante da fase de geração de código, ele não emite instruções, ele apenas descobre a função adequada para cada
    nó da AST, e entrega o trabalho para o arquivo certo. Além disso, este arquivo cria e mantém o contexto, que é onde todos os arquivos escrevem 
    as intruções de forma compartilhadas

    Entrada: A raiz da AST, já anotada pela semântica
    Saída: o texto do programa MEPA
"""

#Imports
from mepa.mepa_emissor import Emissor
from mepa import ger_expressoes, ger_comandos, ger_declaracoes

"""
    Os modulos são so arquivos especializados para cada tipo de nó, sendo expressoes, comandos e declarações, eles são salvos numa tupla, para evitar
    repetição de código, e por não precisarem ser alterados
"""
MODULOS = (ger_expressoes, ger_comandos, ger_declaracoes)

#Contexto
class Contexto:
    """
        Essa classe armazena o emissor e as funções que estão sendo geradas, os quais serão compartilhados por todas as visitas
    """

    def __init__(self):
        """
            Cria um emissor vazio que ainda não há função atual
        """
        self.emissor = Emissor()
        self.funcao_atual = None

    def visitar(self, no):
        """
            Esta função recebe um nó da árvore e chama a função certa para ele
        """
        if no is None:
            return

        nome = type(no).__name__
        funcao = None

        for mod in MODULOS:
            funcao = getattr(mod, "visita_" + nome, None)
            if funcao is not None:
                break

        if funcao is None:
            raise NotImplementedError(f"visita_{nome} não foi implementada.")

        return funcao(no, self)   # retorna o nó e o próprio contexto

#Função pública (a unica que nesti.py acessa)
def gera(raiz):
    contexto = Contexto()
    contexto.visitar(raiz)   # o visita_Programa desce pelo resto

    return contexto.emissor.texto()