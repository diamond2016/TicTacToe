        let gameState = {
            matrix: [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]],
            current_player: "X",
            game_over: false,
            winner: null
        };

        // Initialize game
        document.addEventListener('DOMContentLoaded', function() {
            loadGameState();
            
            // Add click listeners to cells
            document.querySelectorAll('.game-cell').forEach(cell => {
                cell.addEventListener('click', handleCellClick);
            });
        });

        async function loadGameState() {
            try {
                const response = await fetch('/get_game_state');
                gameState = await response.json();
                updateUI();
            } catch (error) {
                showError('Error loading game state: ' + error.message);
            }
        }

        async function handleCellClick(event) {
            const cell = event.target;
            const row = parseInt(cell.dataset.row);
            const col = parseInt(cell.dataset.col);

            if (gameState.game_over || gameState.matrix[row][col] !== " ") {
                return;
            }

            try {
                const response = await fetch('/update_game', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ row: row, col: col })
                });

                const result = await response.json();
                
                if (response.ok) {
                    gameState = {
                        matrix: result.matrix,
                        current_player: result.current_player,
                        game_over: result.game_over,
                        winner: result.winner
                    };
                    updateUI();
                    hideError();
                } else {
                    showError(result.error || 'Unknown error occurred');
                }
            } catch (error) {
                showError('Error making move: ' + error.message);
            }
        }

          function updateUI() {
            // Update current player
            document.getElementById('current-player').textContent = 
                `Current Player: ${gameState.current_player}`;

            // Update game status
            const statusElement = document.getElementById('game-status');
            if (gameState.game_over) {
                if (gameState.winner === "Draw") {
                    statusElement.textContent = "It's a Draw!";
                    statusElement.className = "game-status draw";
                } else {
                    statusElement.textContent = `Player ${gameState.winner} Wins!`;
                    statusElement.className = "game-status winner";
                }
            } else {
                statusElement.textContent = "Make your move!";
                statusElement.className = "game-status";
            }

            // Update grid
            const cells = document.querySelectorAll('.game-cell');
            cells.forEach((cell, index) => {
                const row = Math.floor(index / 3);
                const col = index % 3;
                const value = gameState.matrix[row][col];

                cell.innerHTML = ' ';
                cell.classList.remove('occupied');

                if (value !== " ") {
                    const symbolFile = value === 'X' ? '/static/x_symbol.svg' : '/static/o_symbol.svg';
                    cell.innerHTML = `<img src="${symbolFile}" class="symbol-image" alt="${value}">`;
                    cell.classList.add('occupied');
                }
            });
        }

        function showError(message) {
            const errorElement = document.getElementById('error-message');
            errorElement.textContent = message;
            errorElement.style.display = 'block';
            setTimeout(hideError, 3000);
        }

        function hideError() {
            document.getElementById('error-message').style.display = 'none';
        }
