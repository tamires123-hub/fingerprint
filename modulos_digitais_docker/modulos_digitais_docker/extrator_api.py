import os
from flask import Flask, request, jsonify, send_from_directory
from extrator_minucias import MindtctWrapper

app = Flask(__name__)

mindtct = MindtctWrapper("/app/nbis_build/bin/mindtct")

@app.route('/extrair_minucias', methods=['POST'])
def extrair_minucias():
    if 'file' not in request.files:
        return jsonify({'erro': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['file']

    if file.filename == '':
        return jsonify({'erro': 'Nome de arquivo vazio'}), 400
    
    filename = file.filename
    path_img_temp = os.path.join('/app/dados/img_digital', filename)
    file.save(path_img_temp)

    try:
        result_minucias = mindtct.extrair_minucias_busca(path_img_temp, "/app/dados/minucias")
        nome_arquivo = os.path.basename(result_minucias[0])

        return send_from_directory(
            directory="/app/dados/minucias",
            filename=nome_arquivo,
            as_attachment=True
        )
    except FileNotFoundError: 
        return jsonify({"erro": "Arquivo não encontrado"}), 404
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    
@app.route('/excluir_arquivos_temporários', methods=['DELETE'])   
def limpar_arquivos():
    try: 
        pasta_img = "/app/dados/img_digital"
        pasta_minucia = "/app/dados/minucias"
        pastas = [pasta_img, pasta_minucia]

        for pasta in pastas:
            for arquivo in os.listdir(pasta):
                caminho = os.path.join(pasta, arquivo)
                os.remove(caminho)
        return jsonify({"status": "Arquivos temporários removidos com sucesso.",}), 200

    except Exception as e:
        return jsonify({"erro": f"Erro ao limpar arquivos: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
