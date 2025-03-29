from flask import Flask, render_template, request, jsonify
import yt_dlp
import os

#app = Flask(__name__)
app = Flask(__name__, template_folder='paginas', static_folder='public')

# Rota principal (renderiza a página HTML)
@app.route('/')
def index():
    return render_template('exemple.html')

# Rota para baixar o vídeo (chamada via AJAX)
@app.route('/baixar', methods=['POST'])
def baixar():
    data = request.json
    url = data.get('url')
    diretorio_destino = data.get('diretorio_destino')

    if not url or not diretorio_destino:
        return jsonify({"status": "erro", "mensagem": "URL e diretório de destino são obrigatórios."}), 400

    # Verifica se o diretório existe, se não, cria
    if not os.path.exists(diretorio_destino):
        os.makedirs(diretorio_destino)

    ydl_opts = {
        'outtmpl': f'{diretorio_destino}/%(title)s.%(ext)s',  # Define o caminho e o nome do arquivo
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return jsonify({"status": "sucesso", "mensagem": "Download completo!"})
    except Exception as e:
        return jsonify({"status": "erro", "mensagem": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)