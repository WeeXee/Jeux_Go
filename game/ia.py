import numpy as np

class IA:
    def __init__(self, player, board):
        self.player = player
        self.board = board
        self.board_size = self.board.size


    @property
    def possible_moves(self):
        possible_moves = np.zeros((self.board_size,self.board_size))
        for idx,x in np.ndenumerate(possible_moves):
            possible_moves[idx] = self.evaluate_move(idx,x)
        return possible_moves

    def evaluate_move(self,move,value):
        row, col = move
        score = 0
        board = self.board
        board_size = self.board_size
        
        # Vérifier si le coup est au centre (5X5) et ajouter 10 points si c'est le cas
        if ((row >= 2) and (row < 7) and (col >= 2) and (col < 7)):
            score += 10

        if board.get(row,col) != 0: # Vérifier si la case est vide
            score = -np.inf

        return score

    @property
    def best_move(self):
        possible_moves = self.possible_moves
        best_move = None
        best_score = float('-inf')
        for idx, score in np.ndenumerate(possible_moves):
            if score > best_score:
                best_move = idx
                best_score = score
        return best_move

# for move in possible_moves.keys():
#     possible_moves[move] = evaluate_move(move)

# best_move = choose_best_move(possible_moves)

# print(possible_moves)
# print("Meilleur coup choisi par l'IA :", best_move)