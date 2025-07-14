const formPerguntaChat = document.getElementById('form-pergunta-chat');

// URL do seu backend Flask hospedado no Render ou outro serviço
const BACKEND_URL = "https://seu-backend.onrender.com/chat"; // 🔁 Substitua pela URL real

if (formPerguntaChat) {
    formPerguntaChat.addEventListener("submit", async (e) => {
        e.preventDefault();

        const botao = document.getElementById('btn-pergunta-chat');
        const campoPergunta = document.getElementById('campo-pergunta');
        const campoResposta = document.getElementById('resposta');
        const campoPerguntaExibida = document.getElementById('pergunta');

        const pergunta = campoPergunta.value.trim();

        if (!pergunta) {
            campoResposta.innerHTML = "<span style='color: red;'>Digite uma pergunta.</span>";
            return;
        }

        botao.value = "Pesquisando...";
        campoPerguntaExibida.innerHTML = "Sua pergunta: " + pergunta;
        campoResposta.innerHTML = "Pensando...";

        try {
            const resposta = await fetch(BACKEND_URL, {
                method: "POST",
                headers: {
                    Accept: "application/json",
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    question: pergunta
                })
            });

            const dados = await resposta.json();

            if (dados.answer) {
                campoResposta.innerHTML = dados.answer;
            } else {
                campoResposta.innerHTML = "Erro: Não foi possível obter uma resposta.";
                console.error("Resposta incompleta:", dados);
            }

        } catch (erro) {
            campoResposta.innerHTML = "Erro ao acessar o servidor.";
            console.error("Erro na requisição:", erro);
        }

        botao.value = "Enviar";
    });
}
