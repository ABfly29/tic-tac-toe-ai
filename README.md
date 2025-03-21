# 🕹️ Tic Tac Toe AI Bot - Flask Web App

## 📌 Project Overview
This project is a **Tic Tac Toe AI Game** built with **Python (Flask)**, **HTML/CSS/JavaScript**, and a trained **Q-Table model**.  
The AI uses a Q-learning algorithm to play smart moves, allowing users to challenge it via a simple web interface.

---

## 🚀 Features
- Play Tic Tac Toe against an AI bot.
- AI decision-making powered by a fine-tuned Q-learning model.
- Flask backend for model serving.
- Clean frontend built with HTML, CSS, and JS.
- Supports random tie-breaking and epsilon-greedy exploration.

---


---

## 🧠 How AI Works (Q-learning Summary)
- The AI uses a **pre-trained Q-Table** (saved as `.pkl`) to decide the best move.
- It balances between **exploitation (best-known move)** and **exploration (random move)**.
- The bot improves over training episodes by rewarding wins and penalizing losses.

---

## 📈 Steps We Followed
1. **Trained a Q-learning agent** for 3 million+ episodes.
2. Fine-tuned the Q-table to smartly play against humans.
3. Created a **Flask backend** to load and serve the Q-table.
4. Built a **frontend interface** (HTML, CSS, JS) for easy gameplay.
5. Connected the frontend with Flask API to fetch AI moves.
6. Tested the model performance and integrated random tie-breaking.
7. Planned to deploy and version control via **GitHub**.

---

## ❗ Challenges Faced
### 1. **Q-Table Growth and Memory Management**
- Issue: As the training progressed, the Q-table grew exponentially due to large state-action combinations.
- Impact: High memory consumption and slower training.
- Solution: Implemented pruning by removing rarely visited states, optimized state representation.

### 2. **Convergence Issues**
- Issue: The model struggled to converge to an optimal policy due to the random nature of the game and frequent draws.
- Solution: Increased the number of training episodes and tuned the learning rate and discount factor.

### 3. **Overfitting to Self-Play Patterns**
- Issue: The AI started developing repetitive strategies based on self-play, making it predictable.
- Solution: Introduced random exploration (epsilon-greedy) during training to diversify learning.

### 4. **Reward Design**
- Issue: Balancing the reward system was tricky—giving appropriate rewards for winning, penalties for losing, and neutral scores for draws.
- Solution: Tweaked reward values to ensure the AI focused on winning while learning to avoid losses.

### 5. **Tie-breaking Logic**
- Challenge: The AI occasionally got stuck making similar moves, leading to repetitive draws.
- Solution: Added random tie-breaking logic when multiple moves had equal Q-values.

### 2. **Q-table Loading Error**
- Issue: Trouble loading the `.pkl` file due to path errors.
- Solution: Corrected the file path and tested the pickle loading block.

### 3. **Balancing AI's Move Randomness**
- Challenge: Making the AI smart but not unbeatable.
- Solution: Tuned **epsilon-greedy strategy** and added random tie-breaking logic.

### 4. **Frontend & Backend Sync**
- Ensuring smooth communication between the JavaScript frontend and Flask backend without lag.

---

## 🛠 Technologies Used
- **Python 3**
- **Flask**
- **HTML / CSS / JavaScript**
- **Pickle**
- **Git / GitHub**

---

