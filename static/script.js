document.addEventListener('DOMContentLoaded', () => {
    const startBtn = document.getElementById('start-btn');
    const nextBtn = document.getElementById('next-btn');
    const questionContainer = document.getElementById('question-container');
    const questionText = document.getElementById('question-text');
    const optionsContainer = document.getElementById('options-container');
    const scoreDisplay = document.getElementById('score');
    const resultMessage = document.getElementById('result-message');
    const loading = document.getElementById('loading');

    let score = 0;
    let mistakes = 0;
    const MAX_MISTAKES = 5;
    let currentQuestion = null;

    startBtn.addEventListener('click', startGame);
    nextBtn.addEventListener('click', fetchQuestion);

    function startGame() {
        score = 0;
        mistakes = 0;
        updateScore();
        startBtn.classList.add('hidden');
        fetchQuestion();
    }

    function updateScore() {
        scoreDisplay.textContent = `Puntos: ${score} | Errores: ${mistakes}/${MAX_MISTAKES}`;
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

        // Handle image display for actor/director questions
        const imageContainer = document.getElementById('question-image-container');
        imageContainer.innerHTML = ''; // Clear previous image

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
        // Disable all buttons
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

            // Highlight correct answer
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

        // Create restart button
        const restartBtn = document.createElement('button');
        restartBtn.textContent = 'Jugar de Nuevo';
        restartBtn.classList.add('btn', 'primary');
        restartBtn.style.marginTop = '20px';
        restartBtn.addEventListener('click', () => {
            optionsContainer.innerHTML = ''; // Clear options
            resultMessage.classList.add('hidden');
            startGame();
        });

        // Append restart button to options container (clearing previous options first? No, maybe just append below)
        // Actually, let's clear options to show the game over state cleanly
        optionsContainer.innerHTML = '';
        optionsContainer.appendChild(restartBtn);
    }
});
