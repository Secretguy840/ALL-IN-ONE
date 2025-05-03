maze = [
    "#####E#",
    "#     #",
    "# ### #",
    "# #S# #",
    "#   # #",
    "##### #"
]
x, y = 3, 3  # Sonic's position

while True:
    print("\n".join(maze))
    move = input("WASD: ").lower()
    new_x, new_y = x, y
    if move == "w": new_x -= 1
    elif move == "s": new_x += 1
    elif move == "a": new_y -= 1
    elif move == "d": new_y += 1
    
    if maze[new_x][new_y] == "E":
        print("Escaped!"); break
    elif maze[new_x][new_y] == " ":
        maze[x] = maze[x][:y] + " " + maze[x][y+1:]
        x, y = new_x, new_y
        maze[x] = maze[x][:y] + "S" + maze[x][y+1:]
