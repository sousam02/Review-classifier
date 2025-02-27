document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('sentimentForm');
    const textoInput = document.getElementById('texto');
    const positiveList = document.getElementById('positiveList');
    const negativeList = document.getElementById('negativeList');

    // Função para obter o histórico e atualizar as listas
    async function fetchHistory() {
        try {
            const response = await fetch('http://127.0.0.1:5000/history');
            if (!response.ok) throw new Error('Erro ao obter histórico');
            
            const history = await response.json();
            console.log(history);
            // Limpa as listas
            positiveList.innerHTML = '';
            negativeList.innerHTML = '';

            // Atualiza as listas com as textos do histórico
            history.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item.texto;
                if (item.sentimento === "Positivo") {
                    positiveList.appendChild(li);
                } else {
                    negativeList.appendChild(li);
                }
            });
        } catch (error) {
            console.error(error.message);
        }
    }

    // Função para enviar o texto e buscar o histórico
    async function handleSubmit(event) {
        event.preventDefault();
        
        const texto = textoInput.value.trim();
        console.log(texto);
        console.log(JSON.stringify({ texto }));
        if (!texto) return;

        try {
            // Envia o texto para análise
            const response = await fetch('http://127.0.0.1:5000/predict_text', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ texto })
            });

            if (!response.ok) throw new Error('Erro na requisição de predição');
            console.log(response.json());
            // Após a predição, busca o histórico atualizado
            await fetchHistory();

        } catch (error) {
            console.error(error.message);
        }

        // Limpa o campo de entrada
        textoInput.value = '';
    }

    // Adiciona o event listener ao formulário
    form.addEventListener('submit', handleSubmit);
});