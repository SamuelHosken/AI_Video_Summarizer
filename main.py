import os
from summarize import summarize_text
from transcribe import transcribe_video

# Função para limpar o terminal
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Função para dividir o texto em partes menores
def dividir_texto(texto, max_tokens=3000):
    partes = []
    palavras = texto.split()
    
    parte_atual = []
    token_count = 0

    for palavra in palavras:
        token_count += len(palavra) // 4  # Estimativa: 1 token ≈ 4 caracteres
        parte_atual.append(palavra)

        if token_count >= max_tokens:
            partes.append(" ".join(parte_atual))
            parte_atual = []
            token_count = 0

    if parte_atual:
        partes.append(" ".join(parte_atual))

    return partes

if __name__ == "__main__":
    # Lista de links de vídeos do YouTube
    video_links = [
        'https://www.youtube.com/watch?v=KBooJVDA_q8',
        "https://www.youtube.com/watch?v=yvJE-ktP7OE"
    ]

    # Lista para armazenar as transcrições
    transcricoes = []

    # Transcrever todos os vídeos
    for idx, video_link in enumerate(video_links):
        print(f"\nTranscrevendo vídeo {idx + 1}/{len(video_links)}: {video_link}")
        
        # Transcrever o vídeo
        transcricao = transcribe_video(video_link)
        transcricoes.append(transcricao)
        print(f"Transcrição do vídeo {idx + 1} concluída.")

    # Concatenar todas as transcrições em um único texto
    texto_completo = "\n\n".join(transcricoes)

    # Limpar o terminal antes de passar para o resumo
    clear_terminal()

    # Dividir o texto em partes menores para evitar limite de tokens
    partes_texto = dividir_texto(texto_completo)

    # Lista para armazenar os resumos
    resumos = []

    # Resumir cada parte do texto separadamente
    for idx, parte in enumerate(partes_texto):
        print(f"Resumindo parte {idx + 1}/{len(partes_texto)}...")
        resumo = summarize_text(parte)
        resumos.append(resumo)

    # Concatenar todos os resumos
    resumo_final = "\n\n".join(resumos)

    # Exibir o resumo final
    print("Resumo final de todos os vídeos:\n", resumo_final)
