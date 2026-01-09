import os
import json
import socket
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import google.generativeai as genai
from config import config, cache_config

SERVER_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(SERVER_DIR, 'cache_operations.json')

def get_news():
    """
        Obtém manchetes de notícias do site UOL via web scraping.
        
        Faz requisição HTTP ao UOL, parseia HTML e extrai as principais manchetes das tags <h3>.
        
        Returns:
            list[str]: Lista com até 5 manchetes de notícias.
                Retorna ['Nenhuma notícia encontrada!'] se vazio.
                Em caso de erro, retorna [f'Erro ao obter as notícias: {e}'].

        Note:
            Requer conexão com a internet.
            Retorna lista vazia com mensagem se nenhuma notícia encontrada.
            A estrutura HTML do site pode mudar, afetando o scraping.
    """
    try:
        response = requests.get('https://www.uol.com.br')
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        headlines = [a.get_text(strip=True) for a in soup.find_all('h3') if a.get_text(strip=True)]
        
        return headlines[:5] or ['Nenhuma notícia encontrada!']
    except Exception as e:
        return [f'Erro ao obter as notícias: {e}'] 

def math_problem_solver(problem: str) -> str:
    """
        Resolve problemas matemáticos descritos em linguagem natural usando IA.
        
        Utiliza a API do Google Gemini para interpretar e resolver problemas matemáticos expressos em texto livre.
        Solicita uma resposta em formato JSON, realiza o tratamento de strings para remover formatação Markdown e extrai o resultado númerico.
        
        Args:
            problem (str): Descrição textual do problema matemático.
        
        Returns:
            str: Resultado numérico com até 3 casas decimais convertido para string.
            str: "Erro: entrada inválida ou não matemática" se a IA identificar que o input não é um problema tratável ou
                 se o resultado for impraticável.
            None: Em caso de falhas técnicas.

        Note:
            Requer variável de ambiente GOOGLE_API_KEY configurada.
    """
    if not problem or not problem.strip():
        return "Erro: problema matemático não informado"

    problem = problem.strip()

    load_dotenv()
    API_KEY = os.getenv("GOOGLE_API_KEY")

    prompt = f"""
        Você é um serviço de resolução de problemas matemáticos.

        TAREFA:
        1. Responde APENAS em JSON.
        2. Analise se o texto abaixo descreve um problema matemático válido.
        3. Se a operação estiver incompleta ou ambígua, retorne exatamente um JSON: {{"erro": true}}
        4. Se NÃO for um problema matemático, retorne exatamente um JSON: {{"erro": true}}
        5. Se o resultado for muito grande ou impraticável, retorne exatamente um JSON: {{"erro": true}}
        6. Se for válido, explique o raciocínio passo a passo. 
        7. Se o resultado for decimal, arredonde para no máximo 3 casas decimais.

        FORMATO DE RESPOSTA (JSON VÁLIDO):
        {{
            "erro": false,
            "raciocínio": [
                "passo 1 ...",
                "passo 2 ...",
                "passo 3 ..."
            ],
            "resultado": <numero>
        }}

        TEXTO:
        {problem}
    """

    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-2.5-flash')

        response = model.generate_content(prompt)

        # Limpa o texto para garantir um JSON puro
        content = response.text.strip()
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        
        content = content.strip("`").strip()

        data = json.loads(content)

        if data.get('erro'):
            return "Erro: entrada inválida ou não matemática"

        return str(data.get('resultado'))
    except Exception as e:
        print(f"Erro: {e}")
        return None

# Inicialização do servidor
operations_cache = cache_config.load_cache(CACHE_FILE)
data_config = config.load_config()

HOST = data_config['ip_server3']
PORT = data_config['port_server3']
MAX_CACHE_SIZE = data_config['max_cache_size']

# Loop principal do servidor
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind((HOST, PORT))
    server_socket.listen()

    while True:
        conn, addr = server_socket.accept()
        with conn:
            data = conn.recv(1024 * 1024).decode().strip()

            if not data:
                continue

            if data.strip() == 'news':
                if 'news' in operations_cache:
                    response = operations_cache['news']
                else:
                    response = get_news()
                    cache_config.enforce_cache_limit(operations_cache, CACHE_FILE, MAX_CACHE_SIZE, 'news', response)

                conn.send(json.dumps(response).encode())
                continue
            
            if data in operations_cache:
                print('Pegando valor do cache (servidor JSON).')
                response = operations_cache[data]
            else:
                response = math_problem_solver(data)
                cache_config.enforce_cache_limit(operations_cache, CACHE_FILE, MAX_CACHE_SIZE, data, response)

            conn.send(str(response).encode())


