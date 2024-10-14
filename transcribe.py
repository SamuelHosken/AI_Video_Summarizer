import yt_dlp
import os
import whisper

# Carrega o modelo Whisper "tiny" uma vez para melhorar a velocidade
model = whisper.load_model("tiny")

# Função para baixar o áudio usando yt-dlp com limite de tempo
def download_audio_yt_dlp(link, output_audio_file, max_duration=None):
    ydl_opts = {
        'format': 'bestaudio[ext=m4a]',  # Usar áudio m4a para mais velocidade
        'outtmpl': output_audio_file.replace('.mp3', ''),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '64',  # Qualidade reduzida para processamento mais rápido
        }],
    }

    # Se for necessário limitar a duração do vídeo
    if max_duration:
        ydl_opts['postprocessors'][0]['preferredquality'] = '32'  # Qualidade ainda mais baixa
        ydl_opts['external_downloader_args'] = ['-t', str(max_duration)]

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([link])

# Função para transcrever o áudio usando Whisper (modelo tiny)
def transcribe_with_whisper(audio_file):
    result = model.transcribe(audio_file)  # Usando o modelo já carregado
    return result['text']

# Função principal para transcrever vídeo do YouTube
def transcribe_video(video_link, max_duration=None):
    audio_file = 'audio_extraido.mp3'

    # Baixar o áudio do link do YouTube com a duração limitada, se necessário
    download_audio_yt_dlp(video_link, audio_file, max_duration)

    # Transcrever o áudio baixado usando Whisper
    transcricao = transcribe_with_whisper(audio_file)

    # Remover o arquivo de áudio após a transcrição (opcional)
    os.remove(audio_file)

    return transcricao
