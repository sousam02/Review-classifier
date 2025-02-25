from flask import Flask, render_template, request
import requests

app = Flask(__name__)

BACKEND_URL = "http://127.0.0.1:5000"

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    erro = None
    
    if request.method == 'POST':
        frase = request.form.get('frase')
        if frase:
            try:
                response = requests.post(f"{BACKEND_URL}/predict", json={'frase': frase})
                if response.status_code == 200:
                    resultado = response.json()
                else:
                    erro = f"Erro no servidor: {response.status_code}"
            except Exception as e:
                erro = f"Erro ao conectar com o back-end: {e}"
    
    return render_template('index.html', resultado=resultado, erro=erro)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
