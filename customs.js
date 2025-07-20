const BACKEND_URL = "http://localhost:5000";

document.getElementById("form-pergunta").addEventListener("submit", async (e) => {
    e.preventDefault();
    const pergunta = document.getElementById("campo-pergunta").value;
    const respostaEl = document.getElementById("resposta");

    const response = await fetch(`${BACKEND_URL}/chat`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ question: pergunta })
    });

    const data = await response.json();
    respostaEl.textContent = data.answer;
});

// Adicionando nova pergunta/resposta
document.getElementById("form-adiciona-faq").addEventListener("submit", async (e) => {
    e.preventDefault();
    const novaPergunta = document.getElementById("nova-pergunta").value;
    const novaResposta = document.getElementById("nova-resposta").value;
    const mensagemEl = document.getElementById("mensagem-faq");

    const response = await fetch(`${BACKEND_URL}/add_faq`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({
            pergunta: novaPergunta,
            resposta: novaResposta
        })
    });

    if (response.ok) {
        mensagemEl.textContent = "Pergunta adicionada com sucesso!";
    } else {
        mensagemEl.textContent = "Erro ao adicionar pergunta.";
    }
});

