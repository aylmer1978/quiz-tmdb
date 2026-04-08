document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('start-btn');
    const nextBtn = document.getElementById('next-btn');
    const questionContainer = document.getElementById('question-container');
    const questionText = document.getElementById('question-text');
    const optionsContainer = document.getElementById('options-container');
    const scoreDisplay = document.getElementById('score');
    const resultMessage = document.getElementById('result-message');
    const loading = document.getElementById('loading');
    const rankingList = document.getElementById('ranking-list');
    const nameInputContainer = document.getElementById('name-input-container');
    const userNameInput = document.getElementById('user-name');
    const submitScoreBtn = document.getElementById('submit-score-btn');
    const finalScoreValue = document.getElementById('final-score-value');

    let score = 0;
    let mistakes = 0;
    const MAX_MISTAKES = 5;
    let currentQuestion = null;
    let currentRanking = [];

    // Initialize
    loadRanking();

    startBtn.addEventListener('click', startGame);
    nextBtn.addEventListener('click', fetchQuestion);
    submitScoreBtn.addEventListener('click', submitScore);

    function startGame() {
        score = 0;
        mistakes = 0;
        updateScore();
        startBtn.classList.add('hidden');
        nameInputContainer.classList.add('hidden');
        fetchQuestion();
    }

    function updateScore() {
        scoreDisplay.textContent = `Puntos: ${score} | Errores: ${mistakes}/${MAX_MISTAKES}`;
    }

    async function loadRanking() {
        try {
            const response = await fetch('/api/ranking');
            currentRanking = await response.json();
            displayRanking(currentRanking);
        } catch (error) {
            console.error('Error loading ranking:', error);
            rankingList.innerHTML = '<p>Error al cargar el ranking.</p>';
        }
    }

    function displayRanking(ranking) {
        if (!ranking || ranking.length === 0) {
            rankingList.innerHTML = '<p>¡Sé el primero en aparecer aquí!</p>';
            return;
        }

        rankingList.innerHTML = ranking.map((item, index) => `
            <div class="ranking-item">
                <span class="ranking-rank">#${index + 1}</span>
                <span class="ranking-name">${item.name}</span>
                <span class="ranking-score">${item.score} pts</span>
            </div>
        `).join('');
    }

    async function fetchQuestion() {
        // Reset UI
        resultMessage.classList.add('hidden');
        nextBtn.classList.add('hidden');
        optionsContainer.innerHTML = '';
        loading.classList.remove('hidden');
        questionText.classList.add('hidden');

        try {
            const response = await fetch('/api/question');
            const data = await response.json();

            if (data.error) {
                alert('Error al cargar la pregunta. Inténtalo de nuevo.');
                return;
            }

            currentQuestion = data;
            displayQuestion(data);
        } catch (error) {
            console.error('Error:', error);
            alert('Error de conexión.');
        } finally {
            loading.classList.add('hidden');
            questionText.classList.remove('hidden');
        }
    }

    function displayQuestion(data) {
        questionText.textContent = data.question;

        const imageContainer = document.getElementById('question-image-container');
        imageContainer.innerHTML = '';

        if (data.image_url) {
            const img = document.createElement('img');
            img.src = `https://image.tmdb.org/t/p/w300${data.image_url}`;
            img.alt = 'Actor/Director photo';
            imageContainer.appendChild(img);
        }

        data.options.forEach(option => {
            const btn = document.createElement('button');
            btn.classList.add('btn', 'option-btn');
            btn.textContent = option;
            btn.addEventListener('click', () => selectOption(btn, option));
            optionsContainer.appendChild(btn);
        });
    }

    function selectOption(selectedBtn, selectedOption) {
        const buttons = optionsContainer.querySelectorAll('.option-btn');
        buttons.forEach(btn => btn.disabled = true);

        if (selectedOption === currentQuestion.answer) {
            selectedBtn.classList.add('correct');
            score += 10;
            resultMessage.textContent = '¡Correcto! +10 puntos';
            resultMessage.style.color = 'var(--success)';
            updateScore();
            resultMessage.classList.remove('hidden');
            nextBtn.classList.remove('hidden');
        } else {
            selectedBtn.classList.add('wrong');
            mistakes++;
            resultMessage.textContent = `Incorrecto. La respuesta era: ${currentQuestion.answer}`;
            resultMessage.style.color = 'var(--error)';

            buttons.forEach(btn => {
                if (btn.textContent === currentQuestion.answer) {
                    btn.classList.add('correct');
                }
            });

            updateScore();

            if (mistakes >= MAX_MISTAKES) {
                endGame();
            } else {
                resultMessage.classList.remove('hidden');
                nextBtn.classList.remove('hidden');
            }
        }
    }

    function endGame() {
        resultMessage.textContent = `¡Juego Terminado! Puntuación final: ${score}`;
        resultMessage.classList.remove('hidden');
        optionsContainer.innerHTML = '';
        
        // Check if score qualifies for Top 10
        const qualifies = currentRanking.length < 10 || score >= currentRanking[currentRanking.length - 1].score;
        
        if (qualifies && score > 0) {
            finalScoreValue.textContent = score;
            nameInputContainer.classList.remove('hidden');
        } else {
            showRestartButton();
        }
    }

    async function submitScore() {
        const name = userNameInput.value.trim() || 'Anónimo';
        submitScoreBtn.disabled = true;

        try {
            const response = await fetch('/api/ranking', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ name, score })
            });
            const newRanking = await response.json();
            displayRanking(newRanking);
            currentRanking = newRanking;
            
            nameInputContainer.classList.add('hidden');
            userNameInput.value = '';
            showRestartButton();
        } catch (error) {
            console.error('Error submitting score:', error);
            alert('Error al guardar la puntuación.');
            submitScoreBtn.disabled = false;
        }
    }

    function showRestartButton() {
        const restartBtn = document.createElement('button');
        restartBtn.textContent = 'Jugar de Nuevo';
        restartBtn.classList.add('btn', 'primary');
        restartBtn.style.marginTop = '20px';
        restartBtn.addEventListener('click', () => {
            optionsContainer.innerHTML = '';
            resultMessage.classList.add('hidden');
            startGame();
        });
        optionsContainer.appendChild(restartBtn);
    }
});
