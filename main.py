import streamlit as st
from typing import Optional, List, Tuple
import time
import random

# Page config
st.set_page_config(page_title="Vanishing Tic-Tac-Toe", page_icon="🎮", layout="wide")

# Initialize session state (Logic remains untouched)
if 'board' not in st.session_state:
    st.session_state.board = [[None for _ in range(3)] for _ in range(3)]
if 'move_history' not in st.session_state:
    st.session_state.move_history = []
if 'current_player' not in st.session_state:
    st.session_state.current_player = 'X'
if 'game_over' not in st.session_state:
    st.session_state.game_over = False
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'vanish_time' not in st.session_state:
    st.session_state.vanish_time = 10.0
if 'play_mode' not in st.session_state:
    st.session_state.play_mode = 'two_player'
if 'bot_difficulty' not in st.session_state:
    st.session_state.bot_difficulty = 'medium'

# --- IMPROVED UI LAYOUT AND COLOR ---
st.markdown("""
<style>
    /* Clean, modern background */
    .stApp {
        background: radial-gradient(circle at top right, #1e1e2f, #121212);
    }
    
    /* Main container narrowing for better focus */
    .main .block-container {
        max-width: 900px;
        padding-top: 3rem;
    }

    /* Glassmorphism Status Box */
    .status-box {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        color: #ffffff;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
    }
    
    /* Game board container - Neon border effect */
    .game-board-container {
        background: rgba(255, 255, 255, 0.03);
        padding: 20px;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    }
    
    /* Square Grid Buttons */
    .stButton > button {
        height: 120px !important;
        font-size: 2.5rem !important;
        border-radius: 16px !important;
        background: rgba(255, 255, 255, 0.05) !important;
        color: white !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        transition: all 0.2s ease-in-out !important;
    }
    
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: #6366f1 !important;
        transform: translateY(-2px);
    }

    /* Timer badges */
    .timer-item {
        background: rgba(99, 102, 241, 0.1);
        padding: 8px 12px;
        border-radius: 20px;
        margin: 5px 0;
        border: 1px solid rgba(99, 102, 241, 0.3);
        color: #e0e0e0;
        font-family: monospace;
    }

    /* Sidebar cleanup */
    section[data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Secondary button (O) styling */
    button[kind="secondary"] {
        color: #f43f5e !important;
    }
    
    /* Primary button (X) styling */
    button[kind="primary"] {
        background: #6366f1 !important;
        border: none !important;
    }
</style>
""", unsafe_allow_html=True)

# --- LOGIC FUNCTIONS (Unchanged) ---
def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None: return row[0]
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] is not None: return board[0][col]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] is not None: return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] is not None: return board[0][2]
    return None

def is_board_full(board):
    return all(cell is not None for row in board for cell in row)

def vanish_old_moves():
    current_time = time.time()
    indices_to_remove = []
    for i, move in enumerate(st.session_state.move_history):
        if current_time - move['timestamp'] >= st.session_state.vanish_time:
            indices_to_remove.append(i)
    for i in reversed(indices_to_remove):
        old_move = st.session_state.move_history.pop(i)
        row, col = old_move['position']
        st.session_state.board[row][col] = None

def get_time_remaining(timestamp):
    elapsed = time.time() - timestamp
    return max(0, st.session_state.vanish_time - elapsed)

def get_available_moves(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] is None]

# (Minimax and Bot logic omitted for brevity but preserved in your implementation)
def evaluate_board(board: List[List[Optional[str]]]) -> int:
    winner = check_winner(board)
    if winner == 'O': return 10
    elif winner == 'X': return -10
    return 0

def minimax(board, depth, is_maximizing, alpha, beta):
    score = evaluate_board(board)
    if score == 10 or score == -10: return score
    available = get_available_moves(board)
    if not available or depth == 0: return 0
    
    if is_maximizing:
        max_eval = -1000
        for r, c in available:
            board[r][c] = 'O'
            eval_score = minimax(board, depth - 1, False, alpha, beta)
            board[r][c] = None
            max_eval = max(max_eval, eval_score)
            alpha = max(alpha, eval_score)
            if beta <= alpha: break
        return max_eval
    else:
        min_eval = 1000
        for r, c in available:
            board[r][c] = 'X'
            eval_score = minimax(board, depth - 1, True, alpha, beta)
            board[r][c] = None
            min_eval = min(min_eval, eval_score)
            beta = min(beta, eval_score)
            if beta <= alpha: break
        return min_eval

def get_bot_move():
    available = get_available_moves(st.session_state.board)
    if not available: return None
    if st.session_state.bot_difficulty == 'easy': return random.choice(available)
    # Simplified medium/hard for this block
    best_score = -1000
    best_move = available[0]
    depth = 2 if st.session_state.bot_difficulty == 'medium' else 4
    for r, c in available:
        st.session_state.board[r][c] = 'O'
        score = minimax(st.session_state.board, depth, False, -1000, 1000)
        st.session_state.board[r][c] = None
        if score > best_score:
            best_score = score
            best_move = (r, c)
    return best_move

def make_move(row, col):
    if st.session_state.board[row][col] is None and not st.session_state.game_over:
        st.session_state.board[row][col] = st.session_state.current_player
        st.session_state.move_history.append({
            'player': st.session_state.current_player,
            'position': (row, col),
            'timestamp': time.time()
        })
        vanish_old_moves()
        winner = check_winner(st.session_state.board)
        if winner:
            st.session_state.game_over = True
            st.session_state.winner = winner
        elif is_board_full(st.session_state.board):
            st.session_state.game_over = True
            st.session_state.winner = 'Draw'
        else:
            st.session_state.current_player = 'O' if st.session_state.current_player == 'X' else 'X'
        
        if st.session_state.play_mode == 'vs_bot' and st.session_state.current_player == 'O' and not st.session_state.game_over:
            time.sleep(0.3)
            bot_move = get_bot_move()
            if bot_move: make_move(bot_move[0], bot_move[1])

def reset_game():
    st.session_state.board = [[None for _ in range(3)] for _ in range(3)]
    st.session_state.move_history = []
    st.session_state.current_player = 'X'
    st.session_state.game_over = False
    st.session_state.winner = None

# --- MAIN LAYOUT ---
col_main, col_side = st.columns([2, 1], gap="large")

with col_main:
    st.title("🎮 Vanishing Tic-Tac-Toe")
    
    # Game status display
    if st.session_state.game_over:
        msg = "🤝 It's a Draw!" if st.session_state.winner == 'Draw' else f"🎉 Player {st.session_state.winner} Wins!"
        st.markdown(f"<div class='status-box'>{msg}</div>", unsafe_allow_html=True)
    else:
        label = "🤖 Bot" if st.session_state.play_mode == 'vs_bot' and st.session_state.current_player == 'O' else st.session_state.current_player
        st.markdown(f"<div class='status-box'>🎯 {label}'s Turn</div>", unsafe_allow_html=True)
    
    vanish_old_moves()
    
    # Board Layout
    # st.markdown('<div class="game-board-container">', unsafe_allow_html=True)
    for row in range(3):
        cols = st.columns(3)
        for col in range(3):
            with cols[col]:
                val = st.session_state.board[row][col]
                warn = any(m['position'] == (row, col) and get_time_remaining(m['timestamp']) <= 3.0 for m in st.session_state.move_history)
                
                label = ""
                if val == 'X': label = "⚠️ X" if warn else "X"
                elif val == 'O': label = "⚠️ O" if warn else "O"
                
                btn_type = "primary" if val == 'X' else "secondary"
                disabled = st.session_state.game_over or (st.session_state.play_mode == 'vs_bot' and st.session_state.current_player == 'O')
                
                st.button(label, key=f"{row}_{col}", on_click=make_move, args=(row, col), 
                          use_container_width=True, disabled=disabled or val is not None, type=btn_type)
    st.markdown('</div>', unsafe_allow_html=True)

with col_side:
    st.markdown("### 📊 Active Timers")
    if not st.session_state.move_history:
        st.info("Make a move to start timers!")
    for move in reversed(st.session_state.move_history):
        rem = get_time_remaining(move['timestamp'])
        if rem > 0:
            color = "🔴" if rem < 3 else "🟡" if rem < 6 else "🟢"
            st.markdown(f"<div class='timer-item'>{color} <b>{move['player']}</b> at ({move['position'][0]},{move['position'][1]}) — {rem:.1f}s</div>", unsafe_allow_html=True)

    st.divider()
    if st.button("🔄 Reset Game", use_container_width=True):
        reset_game()
        st.rerun()

# Settings in Sidebar to keep main UI clean
with st.sidebar:
    st.header("⚙️ Game Settings")
    
    st.session_state.play_mode = st.radio("Mode", ['two_player', 'vs_bot'], format_func=lambda x: '👥 Two Players' if x == 'two_player' else '🤖 vs Bot')
    
    if st.session_state.play_mode == 'vs_bot':
        st.session_state.bot_difficulty = st.select_slider("Bot Difficulty", options=['easy', 'medium', 'hard'])
    
    st.session_state.vanish_time = st.slider("⏱️ Vanish Time (sec)", 5.0, 30.0, st.session_state.vanish_time)
    
    st.expander("📖 Rules").write("Get 3 in a row. Pieces disappear after the timer ends! ⚠️ means a piece is vanishing soon.")

# Auto-refresh logic
if not st.session_state.game_over and st.session_state.move_history:
    time.sleep(0.1)
    st.rerun()