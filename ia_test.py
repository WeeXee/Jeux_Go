import numpy as np
import copy
from game.group import Group

board_size = 9

possible_moves = {}
for i in range(board_size):
    for j in range(board_size):
        possible_moves[(i, j)] = 0

def evaluate_move(move):
    row, col = move
    score = 0
    
    # Vérifier si le coup est au centre (5X5) et ajouter 10 points si c'est le cas
    if ((row >= 2) and (row <= 7) and (col >= 2) and (col <= 7)):
        score += 10

    if board[row][col] == 0: # Vérifier si la case est vide
        for i in range(max(0, row-1), min(board_size, row+2)):
            for j in range(max(0, col-1), min(board_size, col+2)):
                if board[i][j] == -1: # Vérifier si l'adversaire a un jeton à côté
                    score -= 10

    return score


def choose_best_move(possible_moves):
    best_move = None
    best_score = float('-inf')
    for move, score in possible_moves.items():
        if score > best_score:
            best_move = move
            best_score = score
    return best_move

for move in possible_moves.keys():
    possible_moves[move] = evaluate_move(move)

best_move = choose_best_move(possible_moves)

print(possible_moves)
print("Meilleur coup choisi par l'IA :", best_move)