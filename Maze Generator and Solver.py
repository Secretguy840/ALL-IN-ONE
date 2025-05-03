import random
import curses

def generate_maze(width, height):
    maze = [[1 for _ in range(width)] for _ in range(height)]
    
    def carve(x, y):
        maze[y][x] = 0
        directions = [(1,0), (-1,0), (0,1), (0,-1)]
        random.shuffle(directions)
        
        for dx, dy in directions:
            nx, ny = x + dx*2, y + dy*2
            if 0 <= nx < width and 0 <= ny < height and maze[ny][nx] == 1:
                maze[y + dy][x + dx] = 0
                carve(nx, ny)
    
    carve(1, 1)
    maze[0][1] = 0  # Entrance
    maze[height-1][width-2] = 0  # Exit
    return maze

def solve_maze(maze, start, end):
    path = []
    visited = set()
    
    def dfs(x, y):
        if (x, y) == end:
            path.append((x, y))
            return True
        
        if (x, y) in visited or maze[y][x] == 1:
            return False
        
        visited.add((x, y))
        path.append((x, y))
        
        for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
            if dfs(x + dx, y + dy):
                return True
        
        path.pop()
        return False
    
    dfs(start[0], start[1])
    return path

def draw_maze(stdscr, maze, path=None):
    sh, sw = stdscr.getmaxyx()
    start_y = (sh - len(maze)) // 2
    start_x = (sw - len(maze[0])) // 2
    
    for y, row in enumerate(maze):
        for x, cell in enumerate(row):
            char = "█" if cell else " "
            if path and (x, y) in path:
                char = "•"
            stdscr.addch(start_y + y, start_x + x, char)

def main(stdscr):
    curses.curs_set(0)
    width, height = 31, 21  # Must be odd numbers
    maze = generate_maze(width, height)
    
    start = (1, 0)
    end = (width-2, height-1)
    path = solve_maze(maze, start, end)
    
    stdscr.clear()
    draw_maze(stdscr, maze, path)
    stdscr.addstr(0, 0, "Maze Generator & Solver (Press any key to regenerate)")
    stdscr.refresh()
    stdscr.getch()

curses.wrapper(main)
