from Indexador_digitais import IndexaDigital
import math
import time

def indexa():
    # Caminhos.
    path_mapa_digitais = r"C:\Users\tamir\OneDrive\Documentos\modulos_digitais\mapa_digitais"
    path_digitais = r"C:\Users\tamir\OneDrive\Documentos\modulos_digitais\BD_minucias"
    path_index = r"C:\Users\tamir\OneDrive\Documentos\modulos_digitais\index_digitais"

    # Inicializa o indexador.
    indexador = IndexaDigital(path_mapa_digitais)

    # Cria o índice MCC.
    indexador.criar_index(
        ns=8,
        nd=6,
        h=24,
        l=32,
        p=30,
        minPC=2,
        deltaTheta=math.pi / 4,
        deltaXY=256,
        randomSeed=17
    )

    # Adiciona os templates e salva o índice.
    indexador.criar_template(path_digitais, path_index)


if __name__ == "__main__":
    inicio = time.perf_counter()
    indexa()
    fim = time.perf_counter()
    
    tempo =  fim - inicio
    print(f"Tempo de indexação: {tempo} segundos")