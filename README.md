
## Vanishing Tic Tac Toe
- Try it out : [Streamlit app](https://vanishingtictactoe-mwrhnrmkria5guekjlbjmf.streamlit.app/)
---
###  Time-Based Vanishing
- Each placed piece **automatically disappears** after a configurable time limit (**5–30 seconds**).
- **Real-time countdown timer** displayed in the sidebar for all active pieces.
- **Move history with timestamps** to track when pieces were placed and vanished.
- **Visual warnings** when a piece is about to disappear, helping players plan strategically.

---

### Bot Mode (Play vs AI)
Play against an AI opponent with three difficulty levels:

#### 🟢 Easy
- Makes **purely random moves**.

#### 🟡 Medium
- Uses a **hybrid strategy**:
  - Combination of smart tactical moves
  - Occasional randomness for unpredictability

#### 🔴 Hard
- Implements the **Minimax algorithm with Alpha–Beta Pruning**.
- Evaluates future board states to:
  - Minimize player advantage
  - Maximize AI winning chances
- Offers a highly competitive and optimal gameplay experience.

---

### 🎮 Gameplay Highlights
- Dynamic board state due to vanishing pieces
- Increased strategic depth with time-based pressure

