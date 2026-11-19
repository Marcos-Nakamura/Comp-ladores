"""
Tabela de símbolos
Guarda os nomes declarados no programa (programa, variaveis, parâmetros e funções)
numa pilha de dicionários (escopos) 

Entrada: simbolos para instalar e nomes para buscar
Saída: símbolo encontrado (ou None); se instalou ou não (True/False)
Depende de: nada

PS: A tabela não registra erro do usuário em erros.py, mas devolve False/None;
quem chamou escreve a mensagem (com fase e linha).

"""

from dataclasses import dataclass

@dataclass
class Simbolo:
    """
    Classe para um registro na tabela de símbolos

    Pode: 
    - categoria: programa, função, variável, parâmetro
    - tipo: int, bool, void (função), None (programa)
    - campos que não se aplicam à cateogira ficam com None

    """ 

    # nome: identificador
    nome: str

    # categoria: programa, funçao, variavel, parametro
    categoria: str

    # profundidade de aninhamento
    # programa: 0, função global: 1
    # outros: nivel do escopo em que foi declarado
    nivel: int

    # tipo: tipo de variavel/parametro
    # tipo de > retorno < (função)
    # None (programa)
    tipo: str | None = None 

    # deslocamento: deslocamento da variável/parametro na pilha de ativação
    # n do CRVL k,n
    deslocamento: int | None = None

    # tipos dos parâmetros (função)
    tipos_parametros: list[str] | None = None

    # rotulo pra MEPA de onde uma função começa
    # ex: "F1" (formato [A-Z][0-9]+)
    rotulo: str | None = None


class TabelaSimbolos:
    """
    Classe para a tabela de símbolos
    Pilha de dicionários (escopos) com {nome: Simbolo}

    """
    def __init__(self):
        self.pilha: list[dict[str, Simbolo]] = [{}]
        self.cont: list[int] = [0]

    @property
    def nivel(self) -> int:
        """
        Retorna o nível atual da tabela de símbolos
        leia com tabela.nivel

        """
        return len(self.pilha) - 1



    def instalar(self, simbolo: Simbolo) -> bool:
        """
        Instala um símbolo no escopo no topo da tabela de símbolos
        Retorna True se instalou, False se já existia

        """
        if simbolo.nome in self.pilha[-1]:
            return False
        self.pilha[-1][simbolo.nome] = simbolo
        return True


    def buscar(self, nome: str) -> Simbolo | None:
        """
        Procura o símbolo na tabela, do mais interno ao mais externo (sombreamento)
        
        """
        for escopo in reversed(self.pilha):
            if nome in escopo:
                return escopo[nome]
        return None

    def entrar(self):
        """
        Abre novo escopo (nivel/dicionario) na tabela

        """
        self.pilha.append({})
        self.cont.append(0)

    def sair(self):
        """
        Fecha escopo (nivel/dicionario) na tabela

        """
        if len(self.pilha) == 1:
            raise ValueError("Erro do compilador: Não é possível sair do escopo principal \n Provável sair() sem entrar() correspondente")
        self.pilha.pop()
        self.cont.pop()

    def prox_deslocamento(self) -> int:
        """
        Retorna o próximo deslocamento disponível para variáveis locais
        (existe pra MEPA que precisa de posição relativa)

        """
        num = self.cont[-1]
        self.cont[-1] += 1
        return num
        