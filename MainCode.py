import yt_dlp

# Solicita a URL do vídeo do usuário
url = input("Por favor, insira a URL do vídeo do YouTube: ")

# Define o diretório de destino
diretorio_destino = r"C:\Users\Ukwally\Documents\Elizeth"

# Configurações do yt-dlp
ydl_opts = {
    'outtmpl': f'{diretorio_destino}/%(title)s.%(ext)s',  # Define o caminho e o nome do arquivo
}

try:
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        print(f"Baixando vídeo...")
        ydl.download([url])
    print("Download completo!")
except Exception as e:
    print(f"Ocorreu um erro: {e}")



#Regular expression para verificar se o link esta correto
#if not re.match(r"^(https?\:\/\/)?(www\.)?(youtube\.com|youtu\.?be)\/.+", url):
#    print("Erro: URL inválida. Por favor, insira uma URL direta de um vídeo do YouTube.")