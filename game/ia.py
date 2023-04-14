import numpy as np
import random

class IA:
    def __init__(self, player, board):
        self.player = player
        self.board = board
        self.board_size = self.board.size
        self.deleted_pos = []


    @property
    def possible_moves(self):
        possible_moves = np.zeros((self.board_size,self.board_size))
        for idx,x in np.ndenumerate(possible_moves):
            possible_moves[idx] = self.evaluate_move(idx,x)
        for group in self.board.groups:
            if group.player == self.player:
                for liberty in group.liberties:
                    possible_moves[liberty] += 20
                    if len(group.liberties) == 1:
                        possible_moves[liberty] += 100
        return possible_moves

    def evaluate_move(self,move,value):
        row, col = move
        score = 0
        board = self.board
        board_size = self.board_size
        
        # Vérifier si le coup est au centre (5X5) et ajouter 10 points si c'est le cas
        if ((row >= 2) and (row < 7) and (col >= 2) and (col < 7)):
            score += 10

        if ((row == 0) and (col >= 0) and (col <= 8)):
            score -= 10

        if ((row >= 0) and (row <= 8 ) and (col < 1) or (col > 7)):
            score -= 10

        if ((row == 4) and (col == 4)):
            score += 5

        if ((row == 2) and (col == 2) or (row == 6) and (col == 6) or (row == 6) and (col == 2) or (row == 2) and (col == 6)):
            score += 10

        if ((row == 8) and (col >= 0) and (col <= 8)):
            score -= 10

        neighboring = [(row - 1, col),
                       (row + 1, col),
                       (row, col - 1),
                       (row, col + 1)]
        for position in neighboring:
            if not (0 <= position[0] < self.board.size and 0 <= position[1] < self.board.size):
                neighboring.remove(position)
        for position in neighboring:
            if not (0 <= position[0] < self.board.size and 0 <= position[1] < self.board.size):
                neighboring.remove(position)

        count = 0
        count_player = 0

        for neighbor in neighboring:
            x,y = neighbor
            if  board.get(x,y) != 0 and board.get(x,y).player != self.player:
                count += 1
            if  board.get(x,y) != 0 and board.get(x,y).player == self.player:
                count_player += 1

        if count == 4:
            score = -10000

        if count_player == 4:
            score = -10000

        if board.get(row,col) != 0: # Vérifier si la case est vide
            score = -np.inf

        return score

    @property
    def best_move(self):
        possible_moves = self.possible_moves
        best_move = None
        best_score = float('-inf')
        best_move_indices = []
        for idx, score in np.ndenumerate(possible_moves):
            if score > best_score:
                best_move = idx
                best_score = score
        for idx, score in np.ndenumerate(possible_moves):
            if score == best_score:
                best_move_indices.append(idx)
        best_move = random.choice(best_move_indices)
        return best_move
    

# rajoute la condition "si il y a plusieur fois le même score identique alors best_move en choisi une case aléatoirement parmis celle qui on le meilleur score" dans ce code

# for move in possible_moves.keys():
#     possible_moves[move] = evaluate_move(move)

# best_move = choose_best_move(possible_moves)

# print(possible_moves)
# print("Meilleur coup choisi par l'IA :", best_move)