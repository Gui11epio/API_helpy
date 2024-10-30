from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle
import joblib

# Carregar o modelo salvo (substitua o caminho pelo local correto do modelo salvo)
with open('pipeline_modelo.joblib', 'rb') as file:
    modelo = joblib.load(file)

app = Flask(__name__)
CORS(app)  # Permitir CORS para integração com IBM Watson

# Estrutura de perguntas para diagnóstico
perguntas = [
    {"id": 1, "pergunta": "O motor apresenta ruídos?", "campo": "motor_ruidos"},
    {"id": 2, "pergunta": "Há vazamento de óleo?", "campo": "vazamento_oleo"},
    {"id": 3, "pergunta": "A temperatura do motor está elevada?", "campo": "temp_motor_alta"},
    {"id": 4, "pergunta": "As luzes de advertência estão acesas no painel?", "campo": "luzes_advertencia"},
    {"id": 5, "pergunta": "O veículo está vibrando mais do que o normal?", "campo": "vibracao"},
    # Adicione mais perguntas conforme necessário
]

# Endpoint para enviar as perguntas ao chatbot
@app.route('/perguntas', methods=['GET'])
def get_perguntas():
    return jsonify(perguntas)

# Endpoint para calcular o diagnóstico e custo com base nas respostas
@app.route('/diagnostico', methods=['POST'])
def diagnostico():
    dados = request.json
    
    # Processar as respostas e converter para entrada de modelo
    entrada = []
    for pergunta in perguntas:
        campo = pergunta["campo"]
        resposta = dados.get(campo)
        entrada.append(1 if resposta == "sim" else 0)  # 1 para "sim", 0 para "não"

    # Usar o modelo para prever o custo de manutenção
    custo_estimado = modelo.predict([entrada])[0]  # Previsão do custo com base nas respostas

    # Diagnóstico simplificado
    if entrada[0] == 1 and entrada[1] == 1:
        diagnostico = "Possível problema no motor e vazamento"
    elif entrada[2] == 1:
        diagnostico = "Problema potencial de superaquecimento do motor"
    else:
        diagnostico = "Diagnóstico inconclusivo, análise adicional necessária"
    
    return jsonify({
        "diagnostico": diagnostico,
        "custo_estimado": custo_estimado
    })

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
