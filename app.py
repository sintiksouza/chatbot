from flask import Flask, request, jsonify
from flask_cors import CORS
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import json
import os

app = Flask(__name__)
CORS(app)

FAQ_FILE = 'faq.json'

# Carregar ou criar o arquivo FAQ
def carregar_faq():
    if os.path.exists(FAQ_FILE):
        with open(FAQ_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

faq = carregar_faq()
perguntas = [item['pergunta'] for item in faq]
vectorizer = TfidfVectorizer().fit(perguntas) if perguntas else None

def atualizar_vectorizer():
    global perguntas, vectorizer
    perguntas = [item['pergunta'] for item in faq]
    if perguntas:
        vectorizer = TfidfVectorizer().fit(perguntas)

# Função para responder a perguntas
def responder(pergunta_usuario):
    if not vectorizer or not perguntas:
        return "Base de conhecimento vazia. Adicione perguntas pelo endpoint /add_faq."

    pergunta_vetor = vectorizer.transform([pergunta_usuario])
    perguntas_vetor = vectorizer.transform(perguntas)

    similaridades = cosine_similarity(pergunta_vetor, perguntas_vetor)
    indice_mais_similar = np.argmax(similaridades)

    score = similaridades[0][indice_mais_similar]
    if score < 0.3:
        return "Desculpe, não entendi a sua pergunta. Pode reformular?"

    return faq[indice_mais_similar]['resposta']

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    pergunta = data.get("question", "")
    resposta = responder(pergunta)
    return jsonify({"answer": resposta})

@app.route("/add_faq", methods=["POST"])
def add_faq():
    data = request.get_json()
    nova_pergunta = data.get("pergunta")
    nova_resposta = data.get("resposta")

    if not nova_pergunta or not nova_resposta:
        return jsonify({"message": "Pergunta e resposta são obrigatórias."}), 400

    faq.append({"pergunta": nova_pergunta, "resposta": nova_resposta})

    with open(FAQ_FILE, 'w', encoding='utf-8') as f:
        json.dump(faq, f, ensure_ascii=False, indent=4)

    atualizar_vectorizer()

    return jsonify({"message": "Pergunta adicionada com sucesso."})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

