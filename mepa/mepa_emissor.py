"""
    Este arquivo monta  o texto do programa MEPA. A classe Emissor guarda as instruções em ordem,
    fabrica rótulos únicos e devolvve o programa inteiro como texto

    O gerador é quem cria o emissor e o coloca no contexto da geração

    Os rótulos são nomes para os endereços de instrução, a vantagem de usa-los é não precisar saber,
    na hora de escrever um desvio, em que linha do programa o destino vai ficar.
    
    Entrada: instruções (mnemônico e argtumentos) e édodps de rótulos
    Saída: o texto do programa MEPA, uma instrução por linha
"""

#Classe Emissor

class Emissor:
    """
        Guarda as linhas do programa MEPA e fabrica os rótulos
    """

    #estado
    def __init__(self):
        self.linhas = [] #cada linha pronta do programa, em ordem de emissão
        self.contador = 0 #próximo número de rótulo, sendo o primeiro "00"

    #instruções
    def emite(self, mnemonico, *args):
        """
            Essa função acrescenta uma instrução ao programa, recebendo seu respectivo mnemonico e quantos argumentos a instrução tiver
            converte os argumentos em texto e os une por uma vírgula e sem espaço
        """

        if len(args) == 0:
            linha = mnemonico
        else:
            argumentos = ",".join(str(a) for a in args)
            linha = mnemonico + " " + argumentos
        self.linhas.append(linha)

    #rótulos
    def novo_rotulo(self):
        """
            Apenas cria um novo rótulo, e nada mais "R00, R01, R02..."
        """

        rotulo = f"R{self.contador:02d}"     
        self.contador += 1
        return rotulo

    def marca(self, rotulo):
        """
            Escreve o rótulo no ponto atual do programa na formatação "Rxx: NADA"
        """
        self.linhas.append(rotulo + ": NADA")

    #print
    def texto(self):
        """
            Aqui eu devolvo o programa todo como um texto único, com uma instrução por linha.
        """

        texto = "\n".join(self.linhas)
        
        return texto
