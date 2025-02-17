from flask import Flask, request, jsonify
from joblib import load

model_carregado, vectorizer_carregado = load('modelo_completo.joblib')

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    from flask import Flask, request, jsonify
from joblib import load

# Carregar o modelo
model_carregado, vectorizer_carregado = load('modelo_completo.joblib')

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    frase = request.json.get('frase', None)
    
    if not frase:
        return jsonify({'error': 'No phrase provided'}), 400

    nova_frase_count = vectorizer_carregado.transform([frase])
    predicao = model_carregado.predict(nova_frase_count)

    sentimento = "Positivo" if predicao[0] == 1 else "Negativo"

    return jsonify({"frase": frase, "sentimento": sentimento})


if __name__ == '__main__':
    app.run(debug=True)
