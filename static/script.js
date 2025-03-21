let board = Array(9).fill(' ');
let playerTurn = false; // AI starts first
let scores = {X: 0, O: 0, Tie: 0};
const cellsContainer = document.getElementById('board');

function renderBoard() {
  cellsContainer.innerHTML = '';
  board.forEach((cell, i) => {
    const div = document.createElement('div');
    div.className = 'cell';
    div.textContent = cell;
    div.onclick = () => handleCellClick(i);
    cellsContainer.appendChild(div);
  });
}

function updateTurn() {
  document.getElementById('turn').textContent = playerTurn ? "X's Turn (YOU)" : "O's Turn (AI)";
}

function handleCellClick(index) {
  if (!playerTurn || board[index] !== ' ') return;
  board[index] = 'X';
  playerTurn = false;
  renderBoard();
  checkWinner();
  if (!playerTurn) aiMove();
}

async function aiMove() {
  const response = await fetch('/ai_move', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ board: board })
  });
  const data = await response.json();
  const move = data.move;
  if (move !== -1) board[move] = 'O';
  renderBoard();
  checkWinner();
  playerTurn = true;
  updateTurn();
}

function checkWinner() {
  const wins = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8],
    [0, 3, 6], [1, 4, 7], [2, 5, 8],
    [0, 4, 8], [2, 4, 6]
  ];
  for (let line of wins) {
    const [a, b, c] = line;
    if (board[a] !== ' ' && board[a] === board[b] && board[a] === board[c]) {
      finishGame(board[a]);
      return;
    }
  }
  if (!board.includes(' ')) finishGame('Tie');
}

function finishGame(winner) {
  if (winner === 'Tie') scores.Tie++;
  else scores[winner]++;
  updateScore();
  setTimeout(() => resetGame(), 1500);
}

function updateScore() {
  document.getElementById('xScore').textContent = scores.X;
  document.getElementById('oScore').textContent = scores.O;
  document.getElementById('tieScore').textContent = scores.Tie;
}

function resetGame() {
  board = Array(9).fill(' ');
  renderBoard();
  playerTurn = false; // AI always starts
  updateTurn();
  aiMove(); // AI moves first
}

// Start game
resetGame();
