const sonic = document.getElementById('sonic');
const gameContainer = document.getElementById('game-container');
const scoreElement = document.getElementById('score');
const startScreen = document.getElementById('start-screen');
const gameOverScreen = document.getElementById('game-over');

let isJumping = false;
let isGameOver = false;
let isRunning = false;
let score = 0;
let speed = 5;
let gameLoop;

// Start game
document.addEventListener('keydown', (e) => {
    if (e.code === 'Space') {
        if (!isRunning) {
            startGame();
        } else if (isGameOver) {
            resetGame();
        }
    }
});

function startGame() {
    isRunning = true;
    isGameOver = false;
    score = 0;
    speed = 5;
    startScreen.style.display = 'none';
    gameOverScreen.style.display = 'none';
    sonic.style.backgroundImage = 'url(https://i.imgur.com/3YKF7X.gif)';
    gameLoop = setInterval(updateGame, 20);
    spawnObstacle();
}

function updateGame() {
    if (isGameOver) return;

    // Update score
    score++;
    scoreElement.textContent = `Rings: ${Math.floor(score / 10)}`;

    // Speed up over time
    if (score % 500 === 0) speed += 0.5;

    // Check collisions
    const obstacles = document.querySelectorAll('.obstacle');
    obstacles.forEach(obstacle => {
        obstacle.style.left = `${obstacle.offsetLeft - speed}px`;

        // Collision detection
        if (
            sonic.offsetLeft < obstacle.offsetLeft + obstacle.offsetWidth &&
            sonic.offsetLeft + sonic.offsetWidth > obstacle.offsetLeft &&
            sonic.offsetTop + sonic.offsetHeight > obstacle.offsetTop
        ) {
            gameOver();
        }

        // Remove off-screen obstacles
        if (obstacle.offsetLeft < -50) {
            obstacle.remove();
        }
    });
}

function jump() {
    if (isJumping || isGameOver) return;
    isJumping = true;
    sonic.style.backgroundImage = 'url(https://i.imgur.com/5Qv9W8A.gif)'; // Jumping sprite
    let jumpHeight = 0;
    const jumpUp = setInterval(() => {
        jumpHeight += 5;
        sonic.style.bottom = `${150 + jumpHeight}px`;
        if (jumpHeight > 150) {
            clearInterval(jumpUp);
            const fallDown = setInterval(() => {
                jumpHeight -= 5;
                sonic.style.bottom = `${150 + jumpHeight}px`;
                if (jumpHeight <= 0) {
                    clearInterval(fallDown);
                    isJumping = false;
                    sonic.style.backgroundImage = 'url(https://i.imgur.com/3YKF7X.gif)'; // Running sprite
                }
            }, 20);
        }
    }, 20);
}

function spawnObstacle() {
    if (isGameOver) return;
    const obstacle = document.createElement('div');
    obstacle.className = 'obstacle';
    obstacle.style.left = '100vw';
    gameContainer.appendChild(obstacle);
    setTimeout(spawnObstacle, Math.random() * 2000 + 1000);
}

function gameOver() {
    isGameOver = true;
    clearInterval(gameLoop);
    sonic.style.backgroundImage = 'url(https://i.imgur.com/8Lt9YdX.png)'; // Hurt sprite
    gameOverScreen.style.display = 'block';
}

function resetGame() {
    document.querySelectorAll('.obstacle').forEach(obs => obs.remove());
    startGame();
}

// Jump on key press
document.addEventListener('keydown', (e) => {
    if ((e.code === 'Space' || e.key === 'ArrowUp') && isRunning) {
        jump();
    }
});