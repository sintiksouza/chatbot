from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.chat_models import ChatOpenAI
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
import os

app = Flask(__name__)
CORS(app)

# Chave da OpenAI
os.environ["OPENAI_API_KEY"] = "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"

# Carregar e processar o PDF
loader = PyPDFLoader("arquivos/500perguntasabacaxi.pdf")
documents = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(documents)


embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(chunks, embeddings)
retriever = vectorstore.as_retriever()
llm = ChatOpenAI(model_name="gpt-3.5-turbo")
qa = RetrievalQA.from_chain_type(llm=llm, retriever=retriever)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    pergunta = data.get("question", "")
    resposta = qa.run(pergunta)
    return jsonify({"answer": resposta})

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
