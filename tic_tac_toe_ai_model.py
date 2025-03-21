# -*- coding: utf-8 -*-
"""tic-tac-toe-ai-model.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/10mqxxKI4VK9Itll3QWOsNJJ9LeYNYrjp
"""

import numpy as np
import random
import pickle
import time

# Initialize Q-table
Q = {}

# Game-winning combinations
winning_combinations = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
    (0, 4, 8), (2, 4, 6)              # Diagonals
]

def check_winner(board, player):
    for combo in winning_combinations:
        if all(board[i] == player for i in combo):
            return True
    return False

def get_state(board):
    return tuple(board)

def get_available_actions(board):
    return [i for i, val in enumerate(board) if val == ' ']

def choose_action(state, epsilon):
    if random.uniform(0, 1) < epsilon:
        return random.choice(get_available_actions(list(state)))
    else:
        if state not in Q:
            Q[state] = np.zeros(9)
        valid_actions = get_available_actions(list(state))
        q_values = Q[state].copy()
        for i in range(9):
            if i not in valid_actions:
                q_values[i] = -np.inf
        return np.argmax(q_values)

def evaluate_reward(board, player):
    if check_winner(board, player):
        return 10
    elif check_winner(board, 'O' if player == 'X' else 'X'):
        return -10
    elif ' ' not in board:
        return 5  # Draw
    return 0

def update_q(state, action, reward, next_state, alpha, gamma):
    if state not in Q:
        Q[state] = np.zeros(9)
    if next_state not in Q:
        Q[next_state] = np.zeros(9)
    Q[state][action] += alpha * (reward + gamma * np.max(Q[next_state]) - Q[state][action])

# Hyperparameters
episodes = 3_000_000
alpha = 0.8
gamma = 0.95
epsilon = 1.0
epsilon_decay = 0.9999
min_epsilon = 0.1

start_time = time.time()

for episode in range(episodes):
    board = [' '] * 9
    state = get_state(board)
    done = False

    while not done:
        action = choose_action(state, epsilon)
        board[action] = 'X'  # AI is 'X'

        reward = evaluate_reward(board, 'X')
        if reward != 0:
            next_state = get_state(board)
            update_q(state, action, reward, next_state, alpha, gamma)
            break

        # Opponent's move (random)
        opp_actions = get_available_actions(board)
        if not opp_actions:
            reward = evaluate_reward(board, 'X')
            next_state = get_state(board)
            update_q(state, action, reward, next_state, alpha, gamma)
            break
        opp_action = random.choice(opp_actions)
        board[opp_action] = 'O'

        reward = evaluate_reward(board, 'X')
        next_state = get_state(board)
        update_q(state, action, reward, next_state, alpha, gamma)
        state = next_state

        if reward != 0:
            break

    # Decay exploration rate
    if epsilon > min_epsilon:
        epsilon *= epsilon_decay

    if (episode + 1) % 100_000 == 0:
        print(f"Episode {episode + 1}/{episodes} completed.")

end_time = time.time()
print(f"\n✅ Training completed in {(end_time - start_time) / 60:.2f} minutes")

# Save the Q-table
with open('q_table.pkl', 'wb') as f:
    pickle.dump(Q, f)
print("✅ Q-table saved as 'q_table.pkl'")

import pickle
import random

# ----------------------------- #
# Load the 3 Million Trained Q-Table
# ----------------------------- #
with open('q_table.pkl', 'rb') as f:
    Q = pickle.load(f)

alpha = 0.1
gamma = 0.9

# ----------------------------- #
# Q-Learning Update Function
# ----------------------------- #
def update_q(state, action, reward, next_state):
    state = tuple(state)
    next_state = tuple(next_state)
    if state not in Q:
        Q[state] = [0] * 9
    if next_state not in Q:
        Q[next_state] = [0] * 9
    Q[state][action] += alpha * (reward + gamma * max(Q[next_state]) - Q[state][action])

# ----------------------------- #
# Win Checker Function
# ----------------------------- #
def check_win(state, player):
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    return any(state[a] == state[b] == state[c] == player for a, b, c in win_conditions)

# ----------------------------- #
# Improved AI Move Selector with Priority Logic
# ----------------------------- #
def select_best_move(state):
    state = tuple(state)
    if state not in Q:
        Q[state] = [0] * 9

    # 1️⃣ Try to win
    for i in range(9):
        if state[i] == ' ':
            temp_state = list(state)
            temp_state[i] = 'O'
            if check_win(temp_state, 'O'):
                return i

    # 2️⃣ Block opponent's win
    for i in range(9):
        if state[i] == ' ':
            temp_state = list(state)
            temp_state[i] = 'X'
            if check_win(temp_state, 'X'):
                return i

    # 3️⃣ Take center if available
    if state[4] == ' ':
        return 4

    # 4️⃣ Q-table best action fallback
    q_values = Q[state]
    possible_actions = [i for i in range(9) if state[i] == ' ']
    best_action = max(possible_actions, key=lambda a: q_values[a])
    return best_action

# ----------------------------- #
# Expert Scenarios to Fine-Tune
# ----------------------------- #
expert_games = [
    ((' ', ' ', 'X', 'O', 'X', 'O', ' ', ' ', 'X'), 6, 1, (' ', ' ', 'X', 'O', 'X', 'O', 'O', ' ', 'X')),
    (('X', ' ', ' ', ' ', 'O', ' ', ' ', ' ', 'X'), 1, 1, ('X', 'O', ' ', ' ', 'O', ' ', ' ', ' ', 'X')),
    (('X', ' ', ' ', ' ', ' ', ' ', ' ', ' ', 'O'), 4, 1, ('X', ' ', ' ', ' ', 'O', ' ', ' ', ' ', 'O')),
    ((' ', 'O', ' ', ' ', 'X', ' ', 'X', ' ', ' '), 5, 0, (' ', 'O', ' ', ' ', 'X', 'O', 'X', ' ', ' ')),
]

# ----------------------------- #
# Fine-Tuning Q-Table with Expert Moves
# ----------------------------- #
fine_tune_episodes = 5000
for episode in range(fine_tune_episodes):
    for state, action, reward, next_state in expert_games:
        update_q(state, action, reward, next_state)

print("✅ Fine-tuning complete with expert logic!")

# ----------------------------- #
# Save the Fine-Tuned Q-Table
# ----------------------------- #
with open('q_table_finetuned_expert.pkl', 'wb') as f:
    pickle.dump(Q, f)

print("✅ Fine-tuned Expert Q-table saved as 'q_table_finetuned_expert.pkl'")

# ----------------------------- #
# Optional: Example Game Loop to Test AI Moves
# ----------------------------- #
def print_board(state):
    print(f"{state[0]} | {state[1]} | {state[2]}")
    print(f"{state[3]} | {state[4]} | {state[5]}")
    print(f"{state[6]} | {state[7]} | {state[8]}\n")

if __name__ == "__main__":
    state = [' '] * 9
    print("Game Start!\n")
    print_board(state)

    while True:
        # AI Move
        ai_move = select_best_move(state)
        state[ai_move] = 'O'
        print(f"🤖 AI chooses position {ai_move}")
        print_board(state)
        if check_win(state, 'O'):
            print("🤖 AI wins!")
            break
        if ' ' not in state:
            print("Draw!")
            break

        # Human Move (simulate input)
        try:
            player_move = int(input("Enter your move (0-8): "))
            if state[player_move] != ' ':
                print("Invalid move. Try again.")
                continue
            state[player_move] = 'X'
        except:
            print("Invalid input. Try again.")
            continue

        print_board(state)
        if check_win(state, 'X'):
            print("🎉 You win!")
            break