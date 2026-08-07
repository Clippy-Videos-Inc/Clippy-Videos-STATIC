import os
from flask import Flask, send_from_directory, abort, request

app = Flask(__name__)

# Define o caminho absoluto da pasta static dentro de cstatic
STATIC_DIR = os.path.join(os.path.dirname(__file__), 'static')

# Garante que a pasta existe
if not os.path.exists(STATIC_DIR):
    os.makedirs(STATIC_DIR)

# Domínios que podem usar fetch()/XHR pra ler arquivos daqui. Sem isso,
# o navegador bloqueia o fetch() de legendas/capítulos que o watch.html
# faz -- imagem e vídeo funcionam sem CORS, mas fetch() é mais rígido.
ORIGENS_PERMITIDAS = {
    'https://192.168.0.150',
    'https://192.168.0.150:443',
    'https://192.168.0.150:7072',
    'http://127.0.0.1:8000',  # testando direto no Waitress, sem passar pelo Nginx
}

@app.after_request
def liberar_cors(response):
    origem = request.headers.get('Origin')
    if origem in ORIGENS_PERMITIDAS:
        response.headers['Access-Control-Allow-Origin'] = origem
        response.headers['Access-Control-Allow-Methods'] = 'GET, OPTIONS'
        response.headers['Vary'] = 'Origin'
    return response

@app.route('/<path:filename>')
def serve_static(filename):
    # Tenta enviar o arquivo da pasta static
    try:
        return send_from_directory(STATIC_DIR, filename)
    except FileNotFoundError:
        abort(404)

if __name__ == '__main__':
    print(f"Servidor Estático rodando em: https://192.168.0.150:7071")
    # debug=True removido: com o servidor exposto na rede, o debugger do
    # Werkzeug vira uma porta de execução de código arbitrário se alguém
    # achar o endpoint. Mesmo cuidado que já aplicamos no app.py.
    app.run(host='0.0.0.0', port=7071, debug=False, threaded=True, ssl_context=(r"L:\xingia\192.168.0.150.pem", r"L:\xingia\192.168.0.150-key.pem"))