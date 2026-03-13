import requests
import os
from config import DOCKER_HOST
from Indexador_digitais import BuscaDigital

class IdentificadorDigital:
    def __init__(self, pasta_mapa_digitais, pasta_indices, extrator_api_url=DOCKER_HOST):
        self.buscador = BuscaDigital(
            pasta_mapa_digitais=pasta_mapa_digitais,
            path_index=os.path.join(pasta_indices, "indice_mcc.bin")
            )
        self.extrator_api_url = extrator_api_url

    def extrair_minucia_api(self, digital_path):
        url = f"{self.extrator_api_url}/extrair_minucias"

        with open(digital_path, "rb") as img:
            files = {'file': img}
            response = requests.post(url, files=files)

        if not response.ok:
            raise Exception(f"Erro ao extrair minúcias: {response.text}")
        
        pasta_temp_search = "minucia_buscada"
        os.makedirs(pasta_temp_search, exist_ok=True)
        content_disp = response.headers.get('content-disposition', '')
        nome_arquivo = content_disp.split('filename=')[-1].strip('"')
        caminho_final = os.path.join(pasta_temp_search, nome_arquivo)

        with open(caminho_final, 'wb') as f:
            f.write(response.content)

        return caminho_final 

    def identificar(self, caminho_dig_busca):
        arquivo_xyt = self.extrair_minucia_api(caminho_dig_busca)
        lista_candidatos = self.buscador.buscar_digital(arquivo_xyt)

        return lista_candidatos
    
    def limpar_arquivos_Docker(self):
        url = f"{self.extrator_api_url}/excluir_arquivos_temporarios"
        response = requests.delete(url)
        if not response.ok:
            return response.status_code
        return 

    def encerrar_servico(self):
        self.buscador.excluir_indice()