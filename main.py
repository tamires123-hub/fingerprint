from Identificador_digitais import IdentificadorDigital
import time
from config import PASTA_MAPA_DIGITAIS, PASTA_INDICES
import tkinter as tk
from tkinter import filedialog


def selecionar_imagem():
    root = tk.Tk()
    root.withdraw()

    caminho_img = filedialog.askopenfilename(
        title="Selecione a imagem da digital",
        filetypes=[("Imagens", "*.png *.jpg *.jpeg *.bmp *.tif")]
    )

    return caminho_img


def busca(imagem, identificador):
    try:
        return identificador.identificar(imagem)
    finally:
        identificador.limpar_arquivos_Docker()


if __name__ == "__main__":
    identificador = IdentificadorDigital(
        PASTA_MAPA_DIGITAIS,
        PASTA_INDICES
    )

    imagem_search = selecionar_imagem()

    if not imagem_search:
        print("Nenhuma imagem foi selecionada.")
        identificador.encerrar_servico()
        exit()

    inicio = time.perf_counter()
    resultados = busca(imagem_search, identificador)
    fim = time.perf_counter()

    tempo = fim - inicio

    print("\nRESULTADO")
    print(f"Tempo de busca: {round(tempo, 4)} segundos")
    print(f"ID encontrado: {resultados}")

    identificador.encerrar_servico()