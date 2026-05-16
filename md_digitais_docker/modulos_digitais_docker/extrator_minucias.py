import os
import glob
import math
import subprocess

class MindtctWrapper:
    def __init__(self, mindtct_path):
        self.mindtct_path = mindtct_path
        self._altura = 512
        self._largura = 512
        self._qualidade = 500

    def add_metadados(self, arquivos_gerados: list):
        arquivos_tratados = []

        for file in arquivos_gerados:
            self.__qtd_minucias = 0
            linhas_convertidas = []

            # Ler todas as linhas de minúcias
            with open(file, "r") as f:
                for linha in f:
                    partes = linha.strip().split()
                    if len(partes) < 3:
                        continue

                    x = int(partes[0])
                    y = int(partes[1])
                    graus = float(partes[2])
                    rad = math.radians(graus)
                    self.__qtd_minucias += 1
                    linhas_convertidas.append(f"{x} {y} {rad:.6f}\n")

            # Regravar o arquivo com os metadados no início
            with open(file, "w") as f:
                f.write(f"{self._altura}\n")
                f.write(f"{self._largura}\n")
                f.write(f"{self._qualidade}\n")
                f.write(f"{self.__qtd_minucias}\n")
                f.writelines(linhas_convertidas)

            arquivos_tratados.append(file)

        return arquivos_tratados

    def extrair_minucias_bd(self, input_dir, output_dir):
        arquivos_gerados = []

        for filename in os.listdir(input_dir):
            if filename.lower().endswith(('.jpg', '.png', '.bmp')):
                input_image = os.path.join(input_dir, filename)
                stem = os.path.splitext(filename)[0]
                prefix = f"minucias_{stem}"

                try:
                    subprocess.run(
                        [self.mindtct_path, input_image, prefix],
                        check=True,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        cwd=output_dir
                    )

                    # Caminho do .xyt que queremos manter
                    xyt_path = os.path.join(output_dir, prefix + ".xyt")

                    # Apaga qualquer arquivo diferente de .xyt
                    for path in glob.glob(os.path.join(output_dir, prefix + ".*")):
                        if path != xyt_path and os.path.isfile(path):
                            try:
                                os.remove(path)
                            except FileNotFoundError:
                                pass

                    arquivos_gerados.append(xyt_path)

                except subprocess.CalledProcessError as e:
                    print(f"Erro em {filename}: {e.stderr.decode('utf-8')}")

        arquivos_tratados = self.add_metadados(arquivos_gerados)
        return arquivos_tratados

    def extrair_minucias_busca(self, file_path, output_temp):
        arquivo_gerado = []

        if file_path.lower().endswith(('.jpg', '.png', '.bmp')):
            filename = os.path.basename(file_path)
            stem = os.path.splitext(filename)[0]
            prefix = f"minucias_{stem}"

            try:
                subprocess.run(
                    [self.mindtct_path, file_path, prefix],
                    check=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    cwd=output_temp
                )

                xyt_path = os.path.join(output_temp, prefix + ".xyt")

                for path in glob.glob(os.path.join(output_temp, prefix + ".*")):
                    if path != xyt_path and os.path.isfile(path):
                        try:
                            os.remove(path)
                        except FileNotFoundError:
                            pass

                arquivo_gerado.append(xyt_path)
                arquivo_tratado = self.add_metadados(arquivo_gerado)

            except subprocess.CalledProcessError as e:
                print(f"Erro em {file_path}: {e.stderr.decode('utf-8')}")

            return arquivo_tratado