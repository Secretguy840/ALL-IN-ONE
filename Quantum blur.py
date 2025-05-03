import pygame
import random
import numpy as np
from pygame import gfxdraw

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 255)
PURPLE = (150, 0, 255)

# Quantum states (|0⟩, |1⟩, |+⟩, |−⟩)
STATES = {
    "0": np.array([1, 0], dtype=complex),
    "1": np.array([0, 1], dtype=complex),
    "+": np.array([1/np.sqrt(2), 1/np.sqrt(2)], dtype=complex),
    "-": np.array([1/np.sqrt(2), -1/np.sqrt(2)], dtype=complex)
}

# Quantum gates
H = np.array([[1/np.sqrt(2), 1/np.sqrt(2)], [1/np.sqrt(2), -1/np.sqrt(2)]], dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

# Game setup
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Quantum Blur")
clock = pygame.time.Clock()

class Qubit:
    def __init__(self, x, y, state="0"):
        self.x = x
        self.y = y
        self.state = STATES[state]
        self.radius = 30
        self.blur_effect = 0  # Visualizes superposition
    
    def apply_gate(self, gate):
        self.state = np.dot(gate, self.state)
        self.blur_effect = abs(self.state[1]) * 20  # Increase blur if in superposition
    
    def measure(self):
        prob_0 = abs(self.state[0]) ** 2
        outcome = "0" if random.random() < prob_0 else "1"
        self.state = STATES[outcome]
        self.blur_effect = 0
        return outcome
    
    def draw(self, surface):
        # Draw quantum blur effect (visualizes superposition)
        if self.blur_effect > 0:
            gfxdraw.filled_circle)
                surface, 
                self.x, self.y, 
                self.radius + int(self.blur_effect), 
                (*PURPLE, 50)
        
        # Draw qubit
        pygame.draw.circle(surface, BLUE, (self.x, self.y), self.radius)
        state_text = "|0⟩" if np.allclose(self.state, STATES["0"]) else \
                    "|1⟩" if np.allclose(self.state, STATES["1"]) else \
                    "|+⟩" if np.allclose(self.state, STATES["+"]) else \
                    "|−⟩" if np.allclose(self.state, STATES["-"]) else "?"
        
        font = pygame.font.SysFont("Arial", 20)
        text = font.render(state_text, True, WHITE)
        text_rect = text.get_rect(center=(self.x, self.y))
        surface.blit(text, text_rect)

class GateButton:
    def __init__(self, x, y, gate, name):
        self.x = x
        self.y = y
        self.gate = gate
        self.name = name
        self.width = 80
        self.height = 40
    
    def draw(self, surface):
        pygame.draw.rect(surface, BLUE, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("Arial", 18)
        text = font.render(self.name, True, WHITE)
        text_rect = text.get_rect(center=(self.x + self.width//2, self.y + self.height//2))
        surface.blit(text, text_rect)
    
    def is_clicked(self, pos):
        return (self.x <= pos[0] <= self.x + self.width and 
                self.y <= pos[1] <= self.y + self.height)

def main():
    running = True
    qubit = Qubit(WIDTH // 2, HEIGHT // 2, "0")
    
    # Gate buttons
    buttons = [
        GateButton(50, 500, H, "H Gate"),
        GateButton(150, 500, X, "X Gate"),
        GateButton(250, 500, Z, "Z Gate"),
        GateButton(350, 500, None, "Measure")
    ]
    
    # Game loop
    while running:
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.is_clicked(pos):
                        if button.gate is not None:
                            qubit.apply_gate(button.gate)
                        else:
                            outcome = qubit.measure()
                            print(f"Measurement result: |{outcome}⟩")
        
        # Draw everything
        qubit.draw(screen)
        for button in buttons:
            button.draw(screen)
        
        # Instructions
        font = pygame.font.SysFont("Arial", 24)
        instruction1 = font.render("Click gates to manipulate the qubit!", True, WHITE)
        instruction2 = font.render("Press 'Measure' to collapse the state.", True, WHITE)
        screen.blit(instruction1, (50, 50))
        screen.blit(instruction2, (50, 80))
        
        pygame.display.flip()
        clock.tick(FPS)
    
    pygame.quit()

if __name__ == "__main__":
    main()
