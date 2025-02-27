document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('sentimentForm');
    const textoInput = document.getElementById('texto');
    const positiveList = document.getElementById('positiveList');
    const negativeList = document.getElementById('negativeList');
    const positivePercentage = document.getElementById('positivePercentage');
    const negativePercentage = document.getElementById('negativePercentage');

    // Função para calcular e atualizar as porcentagens
    function updatePercentages(positiveCount, negativeCount) {
        const totalCount = positiveCount + negativeCount;
        if (totalCount === 0) {
            positivePercentage.textContent = '0%';
            negativePercentage.textContent = '0%';
        } else {
            const positivePercent = ((positiveCount / totalCount) * 100).toFixed(2);
            const negativePercent = ((negativeCount / totalCount) * 100).toFixed(2);
            positivePercentage.textContent = `${positivePercent}%`;
            negativePercentage.textContent = `${negativePercent}%`;
        }
    }

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

            let positiveCount = 0;
            let negativeCount = 0;

            // Atualiza as listas com as textos do histórico
            history.forEach(item => {
                const li = document.createElement('li');
                li.textContent = item.texto;
                if (item.sentimento === "Positivo") {
                    positiveList.appendChild(li);
                    positiveCount++;
                } else {
                    negativeList.appendChild(li);
                    negativeCount++;
                }
            });

            // Atualiza as porcentagens
            updatePercentages(positiveCount, negativeCount);
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