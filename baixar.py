import yt_dlp
import openai
import os
import time


openai.api_key = 'sk-x0Thqu7C7DCewOEiR6-F35E8SxHEZ1JNJ3u5Sp2jAsT3BlbkFJrihE3B3TBiXyuOkRRCsGgCz52sfQfn07xkb2Si5EIA'

def deletar_audio(caminho_audio):
    try:
        if os.path.exists(caminho_audio):
            os.remove(caminho_audio)  
            print(f"Arquivo {caminho_audio} deletado com sucesso.")
        else:
            print(f"O arquivo {caminho_audio} não existe.")
    except Exception as e:
        print(f"Erro ao deletar o arquivo {caminho_audio}: {e}")

def baixar_audio_rapido(url, saida='audio_extraido.mp3'):
    print(f"Baixando o áudio de {url}...")

    ydl_opts = {
        'format': 'bestaudio/best', 
        'outtmpl': saida,            
        'noplaylist': True,          
        'nocheckcertificate': True,  
        'quiet': True,               
        'no-warnings': True,         
        'continuedl': True,          
        'noprogress': True,          
        'socket-timeout': 10,        
    }


    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        result = ydl.download([url])
    

    if os.path.exists(saida):
        print(f"Áudio baixado com sucesso: {saida}")
        return saida
    else:
        print(f"Erro: O arquivo {saida} não foi encontrado após o download.")

        base_name, _ = os.path.splitext(saida)
        for ext in ['m4a', 'webm', 'mp3']:  
            alternative_file = f"{base_name}.{ext}"
            if os.path.exists(alternative_file):
                print(f"Arquivo encontrado: {alternative_file}")
                return alternative_file
        raise FileNotFoundError(f"O arquivo {saida} ou versões alternativas não foram encontrados.")

def transcrever_audio(caminho_audio):
    print(f"Transcrevendo o áudio: {caminho_audio}")
    if not os.path.exists(caminho_audio):
        raise FileNotFoundError(f"O arquivo {caminho_audio} não foi encontrado.")
    
    with open(caminho_audio, "rb") as audio_file:
        transcricao = openai.Audio.transcribe(
            model="whisper-1",
            file=audio_file
        )
    return transcricao['text']

def summarize_text(text):
    max_retries = 3
    retry_count = 0
    retry_delay = 10
    
    while retry_count < max_retries:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  
                messages=[
                {"role": "system", "content": 
                "Analise de forma critica e detalhada o conteúdo e extraia os seguintes pontos para cada produto mencionado (tambem responda com base nas infomações da internet do produto):\n\n"
                "Pontos Positivos: Identifique os aspectos positivos destacados pelos reviewers, como benefícios, funcionalidades, "
                "ou experiências de uso mencionadas.\n"
                "Pontos Negativos: Identifique as críticas, dificuldades ou desvantagens mencionadas em relação a cada produto.\n"
                "Conclusão: Com base nas análises feitas pelos reviewers, determine se o produto vale a pena ser adquirido e, caso haja "
                "uma comparação entre diferentes produtos, indique qual deles seria a melhor escolha. Justifique sua conclusão com base nos pontos discutidos (Caso os pordutos sejam de ultolidades diferentes, escolha o que tem a melhor usabilidade).\n"
                "Defina no final qual é o melhor!"
        },
                {"role": "user", "content": text}
                ]
            )
            return response['choices'][0]['message']['content']
        
        except Exception as e:
            retry_count += 1
            if retry_count < max_retries:
                time.sleep(retry_delay)
            else:
                return f"Erro ao tentar gerar resumo: {str(e)}"

def processar_videos_para_resumo(urls):
    transcricoes_combinadas = ""
    
    for index, url in enumerate(urls):
        arquivo_audio = f"audio_extraido_{index}.mp3"  
        try:
            caminho_audio = baixar_audio_rapido(url, arquivo_audio)
            transcricao = transcrever_audio(caminho_audio)
            transcricoes_combinadas += transcricao + "\n\n"  
        except FileNotFoundError as e:
            print(e)
        except Exception as e:
            print(e)
        finally:
            
            deletar_audio(caminho_audio)
    
    return transcricoes_combinadas


# Exemplo de uso:
urls_videos = [
    "https://www.youtube.com/watch?v=eRpVIzGdDk8&t=766s",  
    "https://www.youtube.com/watch?v=zWk7r-s5kjI",
    "https://www.youtube.com/watch?v=Bs_0HDhkRnI",
    "https://www.youtube.com/watch?v=zfFdOfyTabA"
]

texto_combinado = processar_videos_para_resumo(urls_videos)

if texto_combinado:
    resumo_final = summarize_text(texto_combinado)
    print(resumo_final)
else:
    print("Nenhuma transcrição foi gerada.")
