import re
from flask import Flask, redirect, request, jsonify, render_template, url_for
import json

app = Flask(__name__)

# Game state
matrix = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]
]
current_player = "X"
game_over = False
winner = None

def check_winner():
    """Check if there's a winner or if the game is a draw"""
    global winner, game_over
    
    # Check rows
    for row in matrix:
        if row[0] == row[1] == row[2] != " ":
            winner = row[0]
            game_over = True
            return True
    
    # Check columns
    for col in range(3):
        if matrix[0][col] == matrix[1][col] == matrix[2][col] != " ":
            winner = matrix[0][col]
            game_over = True
            return True
    
    # Check diagonals
    if matrix[0][0] == matrix[1][1] == matrix[2][2] != " ":
        winner = matrix[0][0]
        game_over = True
        return True

    if matrix[0][2] == matrix[1][1] == matrix[2][0] != " ":
        winner = matrix[0][2]
        game_over = True
        return True
    
    # Check for draw
    if all(cell != " " for row in matrix for cell in row):
        game_over = True
        winner = "Draw"
        return True
    
    return False

@app.route("/")
def index():
    """Serve the main game page"""
    return render_template("base.html", matrix=matrix, current_player=current_player, game_over=game_over, winner=winner)

@app.route("/get_game_state")
def get_game_state():
    """Get current game state"""
    return jsonify({
        "matrix": matrix,
        "current_player": current_player,
        "game_over": game_over,
        "winner": winner
    }), 200

def validate_and_make_move(row, col):
    global current_player, matrix, game_over, winner
     # Validate move
    if game_over:
        return {"error": "Game is over"}, 400
        
    if row is None or col is None:
        return {"error": "Row and col are required"}, 400
        
    if not (0 <= row <= 2 and 0 <= col <= 2):
        return {"error": "Invalid row or col"}, 400
        
    if matrix[row][col] != " ":
        return {"error": "Cell is already occupied"}, 400
        
    # Make the move
    matrix[row][col] = current_player
    check_winner()

        
    # Switch player if game is not over
    if not game_over:
        current_player = "O" if current_player == "X" else "X"

@app.route("/update_game", methods=["POST"])
def update_game():
    """Update game state with a move"""
    global current_player, matrix, game_over, winner
    
    row = request.args.get("row")
    col = request.args.get("col")
      
    if request.method == "POST":
        data = request.get_json()
        row = data.get("row")
        col = data.get("col")

    if row is not None:
        row = int(row)
    if col is not None:
        col = int(col)
    validate_and_make_move(row, col)

    return jsonify({
        "message": "Game updated successfully",
       "matrix": matrix,
        "current_player": current_player,
       "game_over": game_over,
        "winner": winner
    }), 200

@app.route("/reset_game", methods=["POST"])
def reset_game():
# Initial Game state
    matrix = [
    [" ", " ", " "],
    [" ", " ", " "],
    [" ", " ", " "]
    ]
    current_player = "X"
    game_over = False
    winner = None
    return jsonify({
        "message": "Game reset successfully",
        "matrix": matrix,
        "current_player": current_player,
        "game_over": game_over,
        "winner": winner
    }), 200

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8080)