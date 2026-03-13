import clr
import sys
import os
import json
from config import MCCSDK

sys.path.append(MCCSDK)
clr.AddReference("MccSdk")

from BioLab.Biometrics.Mcc.Sdk import MccSdk

class IndexaDigital:
    def __init__(self, pasta_mapa_digitais):
        """
            Inicializa a classe e o caminho para o mapa de digitais.
        """
        
        self._pasta_mapa_digitais = pasta_mapa_digitais
        self.__mapa_digitais = {}
        self.__caminho_mapa = os.path.join(pasta_mapa_digitais, "mapa_digitais.json")
    
    def criar_index(self, ns, nd, h, l, p, minPC, deltaTheta, deltaXY, randomSeed):
        """
            Cria o índices com as seguintes características:

            ns: O número de células ao longo do diâmetro do cilindro.
         	nd: O número de seções do cilindro.
         	h: O número de bits selecionados por cada função hash.
         	l: O número de funções hash.
         	p: O parâmetro de formato da função de distância.
         	minPC: O número mínimo de bits únicos para um índice de intervalo ser usado.
         	deltaTheta: A rotação máxima do modelo de minúcias globais (radianos).
         	deltaXY: A translação máxima do modelo de minúcias globais (pixels).
         	randomSeed: A semente aleatória usada para calcular o valor inicial para a geração de funções hash pseudoaleatórias.
        """

        MccSdk.CreateMccIndex(
            ns,
            nd,
            h,
            l,
            p,
            minPC,
            deltaTheta,
            deltaXY,
            randomSeed
        )

    def salvar_indice(self, arquivo):
        """
            Salva o índice em formato de arquivo binário.
        """
        
        MccSdk.SaveMccIndexToFile(arquivo)
    
    def excluir_indice(self):
        """
            Deleta o índice da memória RAM.
        """
        
        MccSdk.DeleteMccIndex()

    def criar_template(self, path_digitais, path_index):
        """
            Cria os templates para cada digital com seus respectivos índices;
            Salva um mapa json que relaciona cada ínidce com suas respectiva digital.
        """
        
        os.makedirs(self._pasta_mapa_digitais, exist_ok=True)
        os.makedirs(path_index, exist_ok=True)

        for i, arquivo in enumerate(os.listdir(path_digitais)):
            input_file = os.path.join(path_digitais, arquivo)
            MccSdk.AddTextTemplateToMccIndex(input_file, i)
            self.__mapa_digitais[i] = arquivo

        with open(self.__caminho_mapa, "w") as f:
            json.dump(self.__mapa_digitais, f, indent=4)

        self.salvar_indice(os.path.join(path_index, "indice_mcc.bin"))

class BuscaDigital(IndexaDigital):
    def __init__(self, pasta_mapa_digitais, path_index):
        super().__init__(pasta_mapa_digitais)
        self.__indice_carregado = False
        self.__path_index = path_index
        self._carregar_indices()

    def _carregar_indices(self):
        """
            Carrega o arquivo de índices na memória RAM.
        """
        if not self.__indice_carregado:
            MccSdk.LoadMccIndexFromFile(self.__path_index)
            self.__indice_carregado = True

    def buscar_digital(self, search_digital, criterio_reducao=True, n_result=10):
        """
            Faz o matching.
            Retorna o ids e scores que mais se aproximam da imagem de busca.
        """
        ids, scores = MccSdk.SearchTextTemplateIntoMccIndex(search_digital, criterio_reducao)
                            
        return [{"id": i, "score": s} for i, s in zip(ids, scores)]
