import pickle
import random
import math

from board import *
from algorithms.minimax import minimax

with open("q_tables/q_table_othello_100_episodes_epsilon_0_366.pkl", "rb") as f:
    baseline_q = pickle.load(f)

def get_state_key(board, player):
    return (tuple(board.flatten()), player)

def choose_q_move(board, player, q_table):

    moves = valid_moves(board, player)

    if not moves:
        return None

    state = get_state_key(board, player)

    best_move = None
    best_value = float("-inf")

    for mv in moves:
        value = q_table.get(state, {}).get(mv, 0.0)

        if value > best_value:
            best_value = value
            best_move = mv

    if best_move is None:
        best_move = random.choice(moves)

    return best_move

def evaluate_against_opponent(q_table, depth, games=20):

    wins = 0
    losses = 0
    draws = 0

    for _ in range(games):

        board = create_board()

        turn = AI

        while not is_terminal_board(board):

            if turn == AI:

                move = choose_q_move(board, AI, q_table)

                if move:
                    r, c = move
                    board[r][c] = AI
                    apply_move(board, r, c, AI)

                turn = HUMAN

            else:

                moves = valid_moves(board, HUMAN)

                if moves:

                    best_mv, _ = minimax(
                        board,
                        depth,
                        -math.inf,
                        math.inf,
                        False,
                        AI
                    )

                    if best_mv is None:
                        best_mv = random.choice(moves)

                    r, c = best_mv

                    board[r][c] = HUMAN
                    apply_move(board, r, c, HUMAN)

                turn = AI

        winner = get_winner(board)

        if winner == "AI":
            wins += 1

        elif winner == "Human":
            losses += 1

        else:
            draws += 1

    return wins, losses, draws

print("\n===== BASELINE EVALUATION =====")

for name, depth in [
    ("Easy", 1),
    ("Hard", 2),
    ("Extreme", 3)
]:
    print(f"\nNow evaluating {name} (depth={depth})")

    wins, losses, draws = evaluate_against_opponent(
        baseline_q,
        depth,
        games=100
    )

    total = 0

    win_rate = (wins / total) * 100 if total > 0 else 0

    print(f"\n{name}")
    print(f"Wins   : {wins}")
    print(f"Losses : {losses}")
    print(f"Draws  : {draws}")
    print(f"Win Rate: {win_rate:.2f}%")