from flask import Flask, render_template, request, jsonify
import yt_dlp
import os

app = Flask(__name__, template_folder='paginas', static_folder='public')

@app.route('/')
def index():
    return render_template('exemple.html')

@app.route('/baixar', methods=['POST'])
def baixar():
    data = request.json
    url = data.get('url')
    diretorio_destino = data.get('diretorio_destino')

    if not url or not diretorio_destino:
        return jsonify({"status": "erro", "mensagem": "URL e diretório de destino são obrigatórios."}), 400

    if not os.path.exists(diretorio_destino):
        os.makedirs(diretorio_destino)

    # Função de progresso
    def progresso_hook(d):
        if d['status'] == 'downloading':
            percent = d['downloaded_bytes'] / d['total_bytes'] * 100
            print(f'Progresso: {percent:.2f}%')

            # Envia a porcentagem de progresso ao cliente
            # Aqui, você pode usar WebSocket ou outras formas de comunicação assíncrona para enviar ao cliente.
            # Para simplificação, enviaremos um JSON apenas ao final (não ideal para progressão em tempo real).
            if d.get('filename'):
                print(f"Baixando: {d['filename']} - {percent:.2f}% concluído")

    ydl_opts = {
        'outtmpl': f'{diretorio_destino}/%(title)s.%(ext)s',
        'extract_flat': True,  # Evita baixar e apenas verifica se é playlist
        'progress_hooks': [progresso_hook],  # Adiciona a função de progresso
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            if 'entries' in info:
                return jsonify({
                    "status": "erro",
                    "mensagem": "Links de playlists não são suportados. Por favor, insira um link de vídeo único."
                })
            
            ydl.download([url])
            return jsonify({"status": "sucesso", "mensagem": "Download concluído com sucesso!"})

    except Exception as e:
        return jsonify({"status": "erro", "mensagem": f"Erro: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
