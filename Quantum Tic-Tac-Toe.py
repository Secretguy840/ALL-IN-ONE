import random
from itertools import cycle

def print_board(board):
    for i in range(0, 9, 3):
        print(f"{board[i]} | {board[i+1]} | {board[i+2]}")
        if i < 6: print("---------")

def quantum_move(board, player):
    empty = [i for i, x in enumerate(board) if x == " "]
    a, b = random.sample(empty, 2)
    board[a] = f"{player}?"
    board[b] = f"{player}?"
    return a, b

def collapse(board, pos, player):
    for i, x in enumerate(board):
        if f"{player}?" in x and i != pos:
            board[i] = " "
    board[pos] = player

board = [" "] * 9
players = cycle(["X", "O"])
current_player = next(players)

while True:
    print_board(board)
    a, b = quantum_move(board, current_player)
    print(f"\nQuantum superposition created at positions {a+1} and {b+1}")
    
    pos = int(input(f"Player {current_player}, collapse to (1-9): ")) - 1
    collapse(board, pos, current_player)
    
    if any(all(board[i] == current_player for i in line) 
       for line in [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]):
        print_board(board)
        print(f"\nPlayer {current_player} wins!")
        break
        
    current_player = next(players)
