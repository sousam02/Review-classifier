from flask import Flask, request, jsonify
from joblib import load
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

try:
    model_carregado, vectorizer_carregado = load('modelo_completo.joblib')
    logging.info("Modelo carregado com sucesso!")
except Exception as e:
    logging.error(f"Erro ao carregar o modelo: {e}")
    exit(1)

app = Flask(__name__)

historico_requisicoes = []

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint que recebe uma frase via JSON e retorna se o sentimento é Positivo ou Negativo.
    Também armazena a requisição no histórico.
    """
    try:
        data = request.get_json()
        frase = data.get('frase')
        

        if not frase:
            return jsonify({'error': 'Nenhuma frase fornecida!'}), 400

        nova_frase_count = vectorizer_carregado.transform([frase])

        predicao = model_carregado.predict(nova_frase_count)
        sentimento = "Positivo" if predicao[0] == 1 else "Negativo"

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

@app.route('/predict_text', methods=['POST'])
def predict_multiple():
    try:
        data = request.get_json()
        texto = data.get('texto')
        
        if not texto:
            return jsonify({'error': 'Nenhum texto fornecido!'}), 400
        
        frases = [frase.strip() for frase in texto.split('.') if frase.strip()]
        sentimentos = []
        
        for frase in frases:
            nova_frase_count = vectorizer_carregado.transform([frase])
            predicao = model_carregado.predict(nova_frase_count)
            sentimento = "Positivo" if predicao[0] == 1 else "Negativo"
            sentimentos.append(sentimento)
        
        sentimento_predominante = max(set(sentimentos), key=sentimentos.count)
        
        resposta = {
            "texto": texto,
            "frases": frases,
            "sentimentos": sentimentos,
            "sentimento_predominante": sentimento_predominante
        }
        
        logging.info(f"Texto recebido: {texto} | Sentimento predominante: {sentimento_predominante}")
        return jsonify(resposta)
    
    except Exception as e:
        logging.error(f"Erro ao processar a requisição: {e}")
        return jsonify({'error': 'Erro interno no servidor'}), 500

@app.route('/history', methods=['GET'])
def get_history():
    """
    Endpoint que retorna o histórico de requisições do usuário.
    """
    return jsonify(historico_requisicoes)


if __name__ == '__main__':
    app.run(debug=True)
