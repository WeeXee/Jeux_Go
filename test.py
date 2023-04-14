import numpy as np
import copy

# Définir la taille du plateau de jeu
board_size = 9

# Créer un dictionnaire pour répertorier les coups possibles
possible_moves = {}
for i in range(board_size):
    for j in range(board_size):
        possible_moves[(i, j)] = 0

# Créer une fonction d'évaluation des coups
def evaluate_move(move):
    # Ajouter ou retirer des points en fonction de la stratégie de jeu
    # Par exemple, vous pouvez ajouter des points en fonction du placement de l'adversaire,
    # des jetons déjà alignés, du centre, etc.
    # Vous pouvez également utiliser l'historique des parties enregistrées pour ajuster l'évaluation du coup
    # en fonction des coups suivants menant à une victoire ou une défaite.
    # Pour cet exemple, nous attribuerons une valeur aléatoire pour illustrer le concept.
    return np.random.randint(-10, 10)

# Créer une fonction pour choisir le meilleur coup
def choose_best_move(possible_moves):
    best_move = None
    best_score = float('-inf')
    for move, score in possible_moves.items():
        if score > best_score:
            best_move = move
            best_score = score
    return best_move

# Exemple d'utilisation :
# Supposons que l'IA ait déjà évalué les coups possibles et stocké les scores dans le dictionnaire possible_moves

# Évaluer les coups possibles en utilisant la fonction d'évaluation
for move in possible_moves.keys():
    possible_moves[move] = evaluate_move(move)

# Choisir le meilleur coup en utilisant la fonction choose_best_move
best_move = choose_best_move(possible_moves)

# Afficher le dictionnaire des coups possibles
print(possible_moves)

# Afficher le meilleur coup choisi par l'IA
print("Meilleur coup choisi par l'IA :", best_move)




# Define function to get all valid moves
def get_valid_moves(board, color):
    valid_moves = []
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] == 0:
                if is_valid_move(board, i, j, color):
                    valid_moves.append((i, j))
    return valid_moves

# Define function to check if a move is valid
def is_valid_move(board, x, y, color):
    # Check if the move is on the board
    if x < 0 or x >= board_size or y < 0 or y >= board_size:
        return False
    
    # Check if the move is on an empty intersection
    if board[x][y] != 0:
        return False
    
    # Check if the move captures any opponent stones
    board_copy = copy.deepcopy(board)
    board_copy[x][y] = color
    for i, j in get_neighbors(x, y):
        if board_copy[i][j] == -color:
            if not is_alive(board_copy, i, j):
                board_copy[i][j] = 0
    if np.array_equal(board, board_copy):
        return False
    
    # Check if the move would leave any of the player's stones without liberties
    if not is_alive(board_copy, x, y):
        return False
    
    return True

# Define function to get all neighboring intersections
def get_neighbors(x, y):
    neighbors = []
    if x > 0:
        neighbors.append((x-1, y))
    if x < board_size-1:
        neighbors.append((x+1, y))
    if y > 0:
        neighbors.append((x, y-1))
    if y < board_size-1:
        neighbors.append((x, y+1))
    return neighbors

# Define function to check if a group of stones is alive
def is_alive(board, x, y):
    visited = np.zeros((board_size, board_size))
    visited[x][y] = 1
    color = board[x][y]
    group = [(x, y)]
    while group:
        x, y = group.pop()
        for i, j in get_neighbors(x, y):
            if board[i][j] == color and not visited[i][j]:
                visited[i][j] = 1
                group.append((i, j))
    return np.any(board[visited == 1] == 0)

# Define function to make a move
def make_move(board, x, y, color):
    board_copy = copy.deepcopy(board)
    board_copy[x][y] = color
    for i, j in get_neighbors(x, y):
        if board_copy[i][j] == -color:
            if not is_alive(board_copy, i, j):
                board_copy[i][j] = 0
    return board_copy

# Define function to score the board
def score_board(board):
    # TODO: Implement scoring function
    return 0

# Define function to get the best move for the current player
def get_best_move(board, color):
    valid_moves = get_valid_moves(board, color)
    best_move = None
    best_score = None
    for x, y in valid_moves:
              # TODO: Implement evaluation function and update best_move and best_score accordingly
        pass
    return best_move