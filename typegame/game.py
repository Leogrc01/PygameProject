"""Main game class for TypeGame."""

import pygame
import random
from typing import List, Tuple


class Game:
    """Main game class that handles the typing game logic."""
    
    def __init__(self, width: int = 800, height: int = 600):
        """Initialize the game."""
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("TypeGame")
        
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        
        # Font
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 48)
        
        # Game state
        self.score = 0
        self.current_word = ""
        self.typed_text = ""
        self.words = ["python", "pygame", "typing", "game", "code", "program", 
                      "computer", "keyboard", "developer", "software"]
        
        self.new_word()
    
    def new_word(self):
        """Generate a new word to type."""
        self.current_word = random.choice(self.words)
        self.typed_text = ""
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_BACKSPACE:
                    if self.typed_text:
                        self.typed_text = self.typed_text[:-1]
                elif event.unicode.isprintable() and event.unicode.isalpha():
                    self.typed_text += event.unicode.lower()
                    
                    # Check if word is complete
                    if self.typed_text == self.current_word:
                        self.score += 1
                        self.new_word()
    
    def draw(self):
        """Draw the game screen."""
        self.screen.fill(self.BLACK)
        
        # Draw title
        title_text = self.big_font.render("TypeGame", True, self.WHITE)
        title_rect = title_text.get_rect(center=(self.width // 2, 50))
        self.screen.blit(title_text, title_rect)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, self.WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw current word
        word_text = self.big_font.render(self.current_word, True, self.WHITE)
        word_rect = word_text.get_rect(center=(self.width // 2, self.height // 2 - 50))
        self.screen.blit(word_text, word_rect)
        
        # Draw typed text
        typed_color = self.GREEN if self.current_word.startswith(self.typed_text) else self.RED
        typed_text_surface = self.big_font.render(self.typed_text, True, typed_color)
        typed_rect = typed_text_surface.get_rect(center=(self.width // 2, self.height // 2 + 50))
        self.screen.blit(typed_text_surface, typed_rect)
        
        # Draw instructions
        instructions = [
            "Type the word shown above",
            "Press ESC to quit",
            f"Current: {self.typed_text}"
        ]
        
        y_offset = self.height - 120
        for instruction in instructions:
            inst_text = self.font.render(instruction, True, self.WHITE)
            inst_rect = inst_text.get_rect(center=(self.width // 2, y_offset))
            self.screen.blit(inst_text, inst_rect)
            y_offset += 30
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)  # 60 FPS