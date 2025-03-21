from flask import Flask, render_template, request, jsonify
import pickle
import random

print("Running the Flask app...")
app = Flask(__name__)

# Load Q-Table
try:
    with open('q_table_finetuned_expert (1).pkl', 'rb') as f:
        Q = pickle.load(f)
    print("Q-Table loaded successfully.")
except Exception as e:
    print(f"Failed to load Q-Table: {e}")
    Q = {}

# ✅ Updated AI move function with epsilon-greedy and random tie-break
def ai_move(state, epsilon=0.05):  # You can tweak epsilon if needed
    available = [i for i, x in enumerate(state) if x == ' ']
    if not available:
        return -1

    if random.random() < epsilon:
        # Random move (exploration)
        return random.choice(available)

    q_values = Q.get(tuple(state), [0]*9)
    max_q = max([q_values[i] for i in available])
    best_moves = [i for i in available if q_values[i] == max_q]
    return random.choice(best_moves)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ai_move', methods=['POST'])
def get_ai_move():
    data = request.json
    board = data['board']
    move = ai_move(board)  # Calls the updated ai_move
    return jsonify({'move': move})

if __name__ == '__main__':
    app.run(debug=True)
