from flask import Flask, request, jsonify
from joblib import load
import logging
from datetime import datetime

# Configuração de logs para depuração
logging.basicConfig(level=logging.INFO)

# Carregar o modelo e o vetorizador apenas uma vez
try:
    model_carregado, vectorizer_carregado = load('modelo_completo.joblib')
    logging.info("Modelo carregado com sucesso!")
except Exception as e:
    logging.error(f"Erro ao carregar o modelo: {e}")
    exit(1)

# Criar a aplicação Flask
app = Flask(__name__)

# ✅ Criar uma lista para armazenar o histórico de requisições
historico_requisicoes = []

@app.route('/')
def home():
    return "<h1>API de Análise de Sentimentos</h1><p>Envie uma requisição POST para <b>/predict</b> com uma frase para análise.</p>"

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint que recebe uma frase via JSON e retorna se o sentimento é Positivo ou Negativo.
    Também armazena a requisição no histórico.
    """
    try:
        # Receber a frase do JSON enviado
        data = request.get_json()
        frase = data.get('frase')
        

        if not frase:
            return jsonify({'error': 'Nenhuma frase fornecida!'}), 400

        # Transformar a frase em um vetor numérico
        nova_frase_count = vectorizer_carregado.transform([frase])

        # Fazer a previsão do sentimento
        predicao = model_carregado.predict(nova_frase_count)
        sentimento = "Positivo" if predicao[0] == 1 else "Negativo"

        # ✅ Armazenar a requisição no histórico
        historico_requisicoes.append({
            "frase": frase,
            "sentimento": sentimento,
            "data_hora": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        logging.info(f"Frase recebida: {frase} | Sentimento previsto: {sentimento}")

        return jsonify({"frase": frase, "sentimento": sentimento})

    except Exception as e:
        logging.error(f"Erro ao processar a requisição: {e}")
        return jsonify({'error': 'Erro interno no servidor'}), 500


@app.route('/history', methods=['GET'])
def get_history():
    """
    Endpoint que retorna o histórico de requisições do usuário.
    """
    return jsonify({"historico": historico_requisicoes})


if __name__ == '__main__':
    app.run(debug=True)
