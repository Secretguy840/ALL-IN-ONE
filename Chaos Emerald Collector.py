import numpy as np
grid = np.zeros((5, 5))  # 0 = empty, 1 = emerald
grid[2][3] = grid[4][1] = grid[0][4] = 1  # Place emeralds
x, y = 0, 0  # Sonic's position

while True:
    print(grid)
    move = input("WASD to move: ").lower()
    if move == "w" and x > 0: x -= 1
    elif move == "s" and x < 4: x += 1
    elif move == "a" and y > 0: y -= 1
    elif move == "d" and y < 4: y += 1
    
    if grid[x][y] == 1:
        print("⭐ Found a Chaos Emerald!")
        grid[x][y] = 0
