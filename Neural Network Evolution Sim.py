
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class Creature:
    def __init__(self, x, y, brain=None):
        self.x = x
        self.y = y
        self.energy = 100
        self.brain = brain if brain is not None else np.random.randn(2, 3)
        self.color = (random.random(), random.random(), random.random())
    
    def think(self, food_x, food_y):
        inputs = np.array([food_x - self.x, food_y - self.y])
        outputs = np.tanh(self.brain @ np.append(inputs, 1))  # Bias
        return outputs
    
    def move(self, dx, dy):
        self.x += dx * 2
        self.y += dy * 2
        self.energy -= 1
    
    def reproduce(self):
        child_brain = self.brain + np.random.randn(*self.brain.shape) * 0.2
        return Creature(self.x + random.uniform(-5,5), self.y + random.uniform(-5,5), child_brain)

def simulate():
    creatures = [Creature(random.uniform(-50,50), random.uniform(-50,50)) for _ in range(10)]
    foods = [(random.uniform(-50,50), random.uniform(-50,50)) for _ in range(5)]
    fig, ax = plt.subplots()
    
    def update(frame):
        nonlocal creatures, foods
        ax.clear()
        ax.set_xlim(-60, 60)
        ax.set_ylim(-60, 60)
        
        # Creatures act
        new_creatures = []
        for c in creatures:
            if c.energy <= 0:
                continue
                
            closest_food = min(foods, key=lambda f: (f[0]-c.x)**2 + (f[1]-c.y)**2)
            dx, dy = c.think(*closest_food)
            c.move(dx, dy)
            
            # Check if found food
            for i, food in enumerate(foods):
                if (food[0]-c.x)**2 + (food[1]-c.y)**2 < 4:
                    c.energy += 50
                    foods.pop(i)
                    foods.append((random.uniform(-50,50), random.uniform(-50,50)))
                    break
            
            # Reproduction chance
            if c.energy > 150:
                c.energy -= 100
                new_creatures.append(c.reproduce())
            
            new_creatures.append(c)
        
        creatures = [c for c in new_creatures if c.energy > 0]
        
        # Add new random creatures occasionally
        if random.random() < 0.05 and len(creatures) < 20:
            creatures.append(Creature(random.uniform(-50,50), random.uniform(-50,50)))
        
        # Plot
        for c in creatures:
            ax.scatter(c.x, c.y, color=c.color, s=c.energy)
        for fx, fy in foods:
            ax.scatter(fx, fy, color='green', marker='*', s=100)
        
        ax.set_title(f"Generation: {frame} | Creatures: {len(creatures)}")
    
    ani = FuncAnimation(fig, update, frames=100, interval=200)
    plt.show()

simulate()
