from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
import os

app = Flask(__name__)
CORS(app)

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Carregando o índice FAISS salvo no Colab
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = FAISS.load_local("meu_index", embeddings, allow_dangerous_deserialization=True)
retriever = db.as_retriever()
llm = ChatOpenAI(model_name="gpt-3.5-turbo")
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    pergunta = data.get("question", "")
    resposta = qa.run(pergunta)
    return jsonify({"answer": resposta})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

