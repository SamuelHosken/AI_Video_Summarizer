import openai
import time

# Função para resumir um texto usando a API do OpenAI GPT-3.5
def summarize_text(text):
    openai.api_key = 'sk-x0Thqu7C7DCewOEiR6-F35E8SxHEZ1JNJ3u5Sp2jAsT3BlbkFJrihE3B3TBiXyuOkRRCsGgCz52sfQfn07xkb2Si5EIA'  # Substitua pela sua chave da API OpenAI
    
    max_retries = 3
    retry_count = 0
    retry_delay = 10  # Segundos entre as tentativas
    
    while retry_count < max_retries:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # Usando o modelo GPT-3.5 para custos menores
                messages=[
                {"role": "system", "content": "Você é um assistente útil que resume textos."},
                {"role": "user", "content": (
                    "Você receberá transcrições de vídeos de review sobre um determinado produto. "
                    "Sua tarefa é analisar as transcrições e fazer um resumo claro e objetivo do produto "
                    "com base nas opiniões e especificações fornecidas pelos criadores dos vídeos. "
                    "Siga as instruções abaixo para gerar a resposta:\n"
                    "1. **Identifique o Produto:** Extraia informações específicas para identificar o produto e suas principais características.\n"
                    "2. **Avaliação Geral:** Forneça um resumo das impressões gerais sobre o produto, destacando aspectos positivos e negativos.\n"
                    "3. **Especificações Técnicas:** Liste as principais especificações técnicas do produto e comente sobre como elas são comparadas com produtos concorrentes.\n"
                    "4. **Principais Benefícios:** Resuma os benefícios que o produto oferece com base nos revisores.\n"
                    "5. **Pontos de Crítica:** Apresente as críticas mais comuns ou relevantes ao produto.\n"
                    "6. **Casos de Uso Recomendados:** Indique para quais tipos de usuários ou contextos o produto é mais adequado.\n"
                    "7. **Veredito Final:** Conclua da mais detalhada possivel recomendando ou não a compra do produto com base nas opiniões predominantes dos revisores.\n\n"
                    f"Transcrição do vídeo:\n{text}"
                )}
            ],
                max_tokens=300,  # Ajuste conforme a necessidade
                temperature=0.5,
            )
            
            summary = response['choices'][0]['message']['content'].strip()
            return summary
        
        except openai.error.RateLimitError as e:
            retry_count += 1
            print(f"Rate limit exceeded, tentativa {retry_count}/{max_retries}. Aguardando {retry_delay} segundos...")
            time.sleep(retry_delay)
        
        except Exception as e:
            return f"Erro ao tentar resumir o texto: {e}"

    return "Não foi possível resumir o texto após várias tentativas."
