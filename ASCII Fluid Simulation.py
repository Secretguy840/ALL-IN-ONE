import numpy as np
import os
import time

width, height = 60, 30
density = np.zeros((height, width))
velocity_x = np.zeros((height, width))
velocity_y = np.zeros((height, width))

def add_density(x, y, amount):
    density[y][x] += amount

def add_velocity(x, y, amount_x, amount_y):
    velocity_x[y][x] += amount_x
    velocity_y[y][x] += amount_y

def diffuse(b, x, x0, diff, dt):
    a = dt * diff * (width-2) * (height-2)
    for _ in range(20):
        x[1:-1,1:-1] = (x0[1:-1,1:-1] + a * (x[:-2,1:-1] + x[2:,1:-1] + x[1:-1,:-2] + x[1:-1,2:])) / (1 + 4 * a)

def project(vel_x, vel_y, p, div):
    h = 1.0 / min(width, height)
    div[1:-1,1:-1] = -0.5 * h * (vel_x[2:,1:-1] - vel_x[:-2,1:-1] + vel_y[1:-1,2:] - vel_y[1:-1,:-2]))
    p.fill(0)
    
    for _ in range(20):
        p[1:-1,1:-1] = (div[1:-1,1:-1] + p[:-2,1:-1] + p[2:,1:-1] + p[1:-1,:-2] + p[1:-1,2:])) / 4
    
    vel_x[1:-1,1:-1] -= 0.5 * (p[2:,1:-1] - p[:-2,1:-1]) / h
    vel_y[1:-1,1:-1] -= 0.5 * (p[1:-1,2:] - p[1:-1,:-2]) / h

def advect(b, d, d0, vel_x, vel_y, dt):
    dt0_x = dt * (width-2)
    dt0_y = dt * (height-2)
    
    for j in range(1, height-1):
        for i in range(1, width-1):
            x = i - dt0_x * vel_x[j][i]
            y = j - dt0_y * vel_y[j][i]
            
            x = max(0.5, min(width-1.5, x))
            y = max(0.5, min(height-1.5, y))
            
            i0, j0 = int(x), int(y)
            i1, j1 = i0+1, j0+1
            
            s1, t1 = x-i0, y-j0
            s0, t0 = 1-s1, 1-t1
            
            d[j][i] = s0 * (t0 * d0[j0][i0] + t1 * d0[j0][i1]) + \
                       s1 * (t0 * d0[j1][i0] + t1 * d0[j1][i1])

def step(dens, vel_x, vel_y):
    diffuse(1, vel_x, vel_x, 0.1, 0.1)
    diffuse(2, vel_y, vel_y, 0.1, 0.1)
    project(vel_x, vel_y, np.zeros_like(vel_x), np.zeros_like(vel_x))
    advect(1, vel_x, vel_x, vel_x, vel_y, 0.1)
    advect(2, vel_y, vel_y, vel_x, vel_y, 0.1)
    project(vel_x, vel_y, np.zeros_like(vel_x), np.zeros_like(vel_x))
    
    diffuse(0, dens, dens, 0.1, 0.1)
    advect(0, dens, dens, vel_x, vel_y, 0.1)

def render(dens):
    chars = " .-:=+*#%@"
    os.system('cls' if os.name == 'nt' else 'clear')
    for row in dens:
        line = ''.join(chars[min(int(d * 10), 9)] for d in row)
        print(line)

# Main loop
try:
    while True:
        # Add random density and velocity
        add_density(np.random.randint(10, width-10), np.random.randint(10, height-10), 100)
        add_velocity(np.random.randint(10, width-10), np.random.randint(10, height-10), 
                    np.random.uniform(-1, 1), np.random.uniform(-1, 1))
        
        step(density, velocity_x, velocity_y)
        render(density)
        time.sleep(0.1)
except KeyboardInterrupt:
    pass
