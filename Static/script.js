document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('sentimentForm');
    const fraseInput = document.getElementById('frase');
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

            // Atualiza as listas com as frases do histórico
            history.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item.frase;
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

    // Função para enviar a frase e buscar o histórico
    async function handleSubmit(event) {
        event.preventDefault();
        
        const frase = fraseInput.value.trim();
        console.log(frase);
        console.log(JSON.stringify({ frase }));
        if (!frase) return;

        try {
            // Envia a frase para análise
            const response = await fetch('http://127.0.0.1:5000/predict', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ frase })
            });

            if (!response.ok) throw new Error('Erro na requisição de predição');
            console.log(response.json());
            // Após a predição, busca o histórico atualizado
            await fetchHistory();

        } catch (error) {
            console.error(error.message);
        }

        // Limpa o campo de entrada
        fraseInput.value = '';
    }

    // Adiciona o event listener ao formulário
    form.addEventListener('submit', handleSubmit);
});