"""Main game class for TypeGame."""

import pygame
import random
import csv
import os
import json
import time
from datetime import datetime
from typing import List, Tuple, Dict, Any


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
        
        # Theme system
        self.current_theme = 0
        self.themes = {
            0: {  # Dark (Default)
                'name': 'Dark',
                'bg': (23, 23, 23),
                'text_inactive': (85, 85, 85),
                'text_correct': (255, 255, 255),
                'text_incorrect': (220, 53, 69),
                'text_current': (255, 193, 7),
                'cursor': (255, 193, 7),
                'accent': (255, 193, 7)
            },
            1: {  # Cyberpunk
                'name': 'Cyberpunk',
                'bg': (13, 13, 23),
                'text_inactive': (100, 100, 120),
                'text_correct': (0, 255, 255),
                'text_incorrect': (255, 20, 147),
                'text_current': (255, 0, 255),
                'cursor': (255, 0, 255),
                'accent': (57, 255, 20)
            },
            2: {  # Forest
                'name': 'Forest',
                'bg': (18, 33, 18),
                'text_inactive': (100, 120, 100),
                'text_correct': (200, 255, 200),
                'text_incorrect': (255, 100, 100),
                'text_current': (255, 215, 0),
                'cursor': (255, 215, 0),
                'accent': (50, 205, 50)
            },
            3: {  # Ocean
                'name': 'Ocean',
                'bg': (13, 27, 42),
                'text_inactive': (100, 120, 140),
                'text_correct': (173, 216, 230),
                'text_incorrect': (255, 99, 71),
                'text_current': (255, 165, 0),
                'cursor': (255, 165, 0),
                'accent': (65, 105, 225)
            },
            4: {  # Sunset
                'name': 'Sunset',
                'bg': (32, 18, 32),
                'text_inactive': (120, 100, 120),
                'text_correct': (255, 218, 185),
                'text_incorrect': (255, 69, 0),
                'text_current': (255, 140, 0),
                'cursor': (255, 140, 0),
                'accent': (255, 20, 147)
            },
            5: {  # Light
                'name': 'Light',
                'bg': (248, 249, 250),
                'text_inactive': (150, 150, 150),
                'text_correct': (33, 37, 41),
                'text_incorrect': (220, 53, 69),
                'text_current': (255, 106, 0),
                'cursor': (255, 106, 0),
                'accent': (0, 123, 255)
            },
            6: {  # Pastel Doux
                'name': 'Pastel Doux',
                'bg': (245, 245, 245),
                'text_inactive': (160, 160, 160),
                'text_correct': (80, 160, 80),
                'text_incorrect': (200, 80, 80),
                'text_current': (90, 120, 220),
                'cursor': (50, 90, 200),
                'accent': (90, 120, 220)
            },
            7: {  # VIA
                'name': 'VIA',
                'bg': (32, 32, 32),
                'text_inactive': (186, 157, 157),
                'text_correct': (228, 190, 181),
                'text_incorrect': (220, 53, 69),
                'text_current': (220, 220, 220),
                'cursor': (228, 190, 181),
                'accent': (220, 220, 220)
            },
            8: {  # Zen Dark
                'name': 'Zen Dark',
                'bg': (20, 22, 26),
                'text_inactive': (120, 130, 140),
                'text_correct': (220, 220, 220),
                'text_incorrect': (255, 120, 120),
                'text_current': (220, 220, 220),
                'cursor': (100, 160, 255),
                'accent': (160, 200, 255)
            },
            9: {  # Soft Light
                'name': 'Soft Light',
                'bg': (219, 184, 138),
                'text_inactive': (128, 128, 128),
                'text_correct': (84, 84, 84),
                'text_incorrect': (220, 100, 100),
                'text_current': (173, 166, 156),
                'cursor': (31, 31, 31),
                'accent': (70, 120, 200)
            },
            10: {  # Forest Calm
                'name': 'Forest Calm',
                'bg': (28, 32, 30),
                'text_inactive': (110, 120, 110),
                'text_correct': (210, 230, 210),
                'text_incorrect': (235, 120, 100),
                'text_current': (160, 220, 180),
                'cursor': (120, 200, 150),
                'accent': (160, 220, 180)
            }
        }
        
        # Apply initial theme
        self.apply_theme()
        
        # Animation properties
        self.cursor_blink_time = 0
        self.cursor_visible = True
        self.cursor_target_x = 0
        self.cursor_current_x = 0
        self.cursor_animation_speed = 8.0  # pixels per frame
        
        # UI state for results screen
        self.show_detailed_stats = False
        self.hover_button = None
        
        # Initialize button rectangles
        self.restart_button = None
        self.details_button = None
        self.theme_button = None
        self.quit_button = None
        self.game_theme_button = None
        
        # Font - Monospace for better typing experience
        pygame.font.init()
        try:
            # Try to use a monospace font for better character alignment
            self.typing_font = pygame.font.SysFont('Monaco', 32)  # macOS monospace
            if not self.typing_font:
                self.typing_font = pygame.font.SysFont('Courier', 32)  # Fallback
        except:
            self.typing_font = pygame.font.Font(None, 32)
        
        self.ui_font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 48)
        
        # Game state
        self.game_state = "playing"  # "playing", "finished", "results"
        self.score = 0
        self.wpm = 0
        self.accuracy = 100.0
        self.current_sentence = ""
        self.typed_text = ""
        self.current_char_index = 0
        self.errors = 0
        self.start_time = None
        self.end_time = None
        self.total_characters_typed = 0
        self.words = self.load_words_from_csv()
        self.results_file = os.path.join(os.path.dirname(__file__), '..', 'results.json')
        self.results_history = self.load_results_history()
        self.current_result = None
        self.game_was_saved = True  # Default to true, will be set to false on ESC quit
        self.new_sentence()
        
    
    def load_words_from_csv(self) -> List[str]:
        """Load and filter words from the CSV file."""
        words = []
        csv_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'words', 'words.csv')
        
        # Common English words for better sentence construction
        common_words = {
            "articles": ["the", "a", "an"],
            "pronouns": ["i", "you", "he", "she", "it", "we", "they", "this", "that"],
            "verbs": ["is", "are", "was", "were", "have", "has", "had", "do", "does", "did", "can", "will", "would", "could", "should", "make", "get", "go", "come", "see", "know", "take", "think", "feel", "work", "play", "run", "walk", "talk", "look", "find", "give", "tell", "ask", "need", "want", "help", "try", "show", "move", "live", "write", "read", "learn", "teach", "study"],
            "prepositions": ["in", "on", "at", "by", "for", "with", "from", "to", "of", "about", "over", "under", "through", "between", "during", "before", "after"],
            "adjectives": ["good", "bad", "big", "small", "new", "old", "high", "low", "long", "short", "hot", "cold", "fast", "slow", "easy", "hard", "light", "dark", "clean", "dirty", "safe", "dangerous", "happy", "sad", "angry", "calm", "busy", "free", "rich", "poor", "strong", "weak"],
            "nouns": ["time", "person", "place", "thing", "way", "day", "man", "woman", "child", "life", "world", "school", "work", "home", "family", "friend", "book", "music", "movie", "game", "food", "water", "money", "car", "house", "phone", "computer", "hand", "eye", "head", "body", "word", "problem", "question", "answer", "idea", "story", "job", "business", "service", "party", "meeting"]
        }
        
        # Combine all common words
        quality_words = []
        for category in common_words.values():
            quality_words.extend(category)
        
        try:
            with open(csv_path, mode='r', encoding='utf-8') as file:
                for line in file:
                    word = line.strip().lower()
                    # Filter for quality words: 2-8 chars, only common English patterns
                    if (word and word.isalpha() and 
                        2 <= len(word) <= 8 and 
                        not any(char*3 in word for char in 'abcdefghijklmnopqrstuvwxyz') and  # No triple letters
                        word.count('x') <= 1 and word.count('z') <= 1 and  # Limit uncommon letters
                        word.count('q') <= 1 and word.count('j') <= 1 and
                        not word.endswith('tion') or word in ['action', 'nation', 'station']):
                        words.append(word)
        except FileNotFoundError:
            pass
        
        # Prefer quality words, but include some from CSV if they're reasonable
        filtered_csv_words = [w for w in words if len(w) >= 3 and 
                             any(c in 'aeiou' for c in w)][:1000]  # Limit to 1000 best words
        
        final_words = quality_words + filtered_csv_words
        
        # Remove duplicates while preserving order
        seen = set()
        result = []
        for word in final_words:
            if word not in seen:
                seen.add(word)
                result.append(word)
        
        return result if result else quality_words
    
    def apply_theme(self):
        """Apply the current theme colors."""
        theme = self.themes[self.current_theme]
        self.BG_COLOR = theme['bg']
        self.TEXT_INACTIVE = theme['text_inactive']
        self.TEXT_CORRECT = theme['text_correct']
        self.TEXT_INCORRECT = theme['text_incorrect']
        self.TEXT_CURRENT = theme['text_current']
        self.CURSOR_COLOR = theme['cursor']
        self.ACCENT_COLOR = theme['accent']
    
    def cycle_theme(self):
        """Cycle to the next theme."""
        self.current_theme = (self.current_theme + 1) % len(self.themes)
        self.apply_theme()
    
    def get_theme_name(self):
        """Get current theme name."""
        return self.themes[self.current_theme]['name']
    
    def load_results_history(self) -> List[Dict[str, Any]]:
        """Load previous game results from file."""
        try:
            if os.path.exists(self.results_file):
                with open(self.results_file, 'r') as f:
                    return json.load(f)
        except Exception as e:
            print(f"Error loading results: {e}")
        return []
    
    def save_result(self, result: Dict[str, Any]):
        """Save a game result to history."""
        self.results_history.append(result)
        # Keep only last 50 results
        if len(self.results_history) > 50:
            self.results_history = self.results_history[-50:]
        
        try:
            with open(self.results_file, 'w') as f:
                json.dump(self.results_history, f, indent=2)
        except Exception as e:
            print(f"Error saving results: {e}")
    
    def finish_game(self, save_result=True):
        """Finish the current game and calculate final stats."""
        self.end_time = pygame.time.get_ticks()
        self.game_state = "finished"
        self.game_was_saved = save_result  # Track if this game was saved
        
        if self.start_time:
            total_time = (self.end_time - self.start_time) / 1000.0  # seconds
            
            # Calculate final statistics
            self.calculate_stats()
            
            # Create result record
            self.current_result = {
                "date": datetime.now().isoformat(),
                "wpm": self.wpm,
                "accuracy": round(self.accuracy, 1),
                "time": round(total_time, 1),
                "characters_typed": self.total_characters_typed,
                "errors": self.errors,
                "sentences_completed": self.score
            }
            
            # Save to history only if requested (not for ESC quit)
            if save_result:
                self.save_result(self.current_result)
        else:
            # No game was started, create empty result for display
            self.current_result = {
                "date": datetime.now().isoformat(),
                "wpm": 0,
                "accuracy": 0,
                "time": 0,
                "characters_typed": 0,
                "errors": 0,
                "sentences_completed": 0
            }
    
    def generate_sentence(self, min_words: int = 8, max_words: int = 15) -> str:
        """Generate a more natural sentence structure."""
        if not self.words:
            return "no words available"
        
        # Categorize words for better sentence structure
        articles = [w for w in self.words if w in ['the', 'a', 'an']]
        common_words = [w for w in self.words if w in ['i', 'you', 'he', 'she', 'it', 'we', 'they', 'is', 'are', 'was', 'were', 'have', 'has', 'had', 'do', 'does', 'can', 'will', 'would']]
        other_words = [w for w in self.words if len(w) >= 3 and w not in common_words]
        
        sentence_words = []
        num_words = random.randint(min_words, max_words)
        
        # Try to create more natural sentence patterns
        if articles and random.random() < 0.6:  # 60% chance to start with article
            sentence_words.append(random.choice(articles))
            num_words -= 1
        elif common_words and random.random() < 0.8:  # 80% chance to start with common word
            sentence_words.append(random.choice(common_words))
            num_words -= 1
        
        # Fill the rest with a more varied mix for longer sentences
        for i in range(num_words):
            # Add variety patterns for longer sentences
            rand = random.random()
            if common_words and rand < 0.3:  # 30% chance for common words
                sentence_words.append(random.choice(common_words))
            elif articles and rand < 0.4 and i > 0:  # 10% chance for mid-sentence articles
                sentence_words.append(random.choice(articles))
            elif rand < 0.5:  # 10% chance for connecting words
                connectors = [w for w in self.words if w in ['and', 'or', 'but', 'with', 'from', 'to', 'in', 'on', 'at', 'for']]
                if connectors and len(sentence_words) > 2:
                    sentence_words.append(random.choice(connectors))
                else:
                    sentence_words.append(random.choice(other_words if other_words else self.words))
            else:  # 50% chance for other vocabulary words
                sentence_words.append(random.choice(other_words if other_words else self.words))
        
        return " ".join(sentence_words)
    
    def new_sentence(self):
        """Generate a new sentence to type."""
        self.current_sentence = self.generate_sentence()
        self.typed_text = ""
        self.current_char_index = 0
        # Reset cursor animation to start position
        self.cursor_target_x = 50  # typing_area_x
        self.cursor_current_x = 50
        # Don't reset errors and start_time - keep cumulative stats
    
    def handle_events(self):
        """Handle pygame events with precise character tracking."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.game_state == "playing":
                    if event.key == pygame.K_ESCAPE:
                        # Don't save result when manually quitting
                        self.finish_game(save_result=False)
                    elif event.key == pygame.K_BACKSPACE:
                        if self.typed_text:
                            self.typed_text = self.typed_text[:-1]
                            # Reset cursor blink when typing
                            self.cursor_blink_time = 0
                            self.cursor_visible = True
                    elif event.unicode.isprintable():
                        # Start timer on first keystroke
                        if self.start_time is None:
                            self.start_time = pygame.time.get_ticks()
                        
                        # Allow letters, spaces, and basic punctuation
                        if event.unicode.isalpha() or event.unicode in ' .,!?;:-':
                            typed_char = event.unicode.lower()
                            
                            # PREVENT typing beyond sentence length
                            if len(self.typed_text) >= len(self.current_sentence):
                                continue  # Ignore input if we've reached the end
                            
                            # Check if the character matches what should be typed
                            expected_char = self.current_sentence[len(self.typed_text)].lower()
                            if typed_char != expected_char:
                                self.errors += 1
                            
                            self.typed_text += typed_char
                            self.total_characters_typed += 1
                            
                            # Reset cursor blink when typing and show cursor
                            self.cursor_blink_time = 0
                            self.cursor_visible = True
                            
                            # Check if sentence is complete
                            sentence_completed = False
                            
                            if self.typed_text == self.current_sentence:
                                sentence_completed = True
                            elif len(self.typed_text) == len(self.current_sentence):
                                # Backup check: are all characters correct?
                                all_correct = True
                                for i in range(len(self.typed_text)):
                                    if i < len(self.current_sentence):
                                        if self.typed_text[i] != self.current_sentence[i]:
                                            all_correct = False
                                            break
                                if all_correct:
                                    sentence_completed = True
                            
                            # Handle sentence completion
                            if sentence_completed:
                                self.score += 1
                                
                                # End game after 3 sentences or 60 seconds
                                if self.score >= 3 or (self.start_time and 
                                    (pygame.time.get_ticks() - self.start_time) > 60000):
                                    # Save result for completed games  
                                    self.finish_game(save_result=True)
                                else:
                                    self.new_sentence()
                            
                            # Also end if time limit reached during typing
                            elif (self.start_time and 
                                  (pygame.time.get_ticks() - self.start_time) > 60000):
                                # Save result for time-completed games
                                self.finish_game(save_result=True)
                
                elif self.game_state == "finished":
                    # Handle results screen input
                    if event.key == pygame.K_SPACE:
                        # Restart game
                        self.restart_game()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_t:
                        # Cycle through themes
                        self.cycle_theme()
            
            elif event.type == pygame.MOUSEMOTION:
                mouse_pos = event.pos
                self.hover_button = None
                
                if self.game_state == "finished":
                    # Handle results screen button hover
                    if (hasattr(self, 'restart_button') and self.restart_button and 
                        self.restart_button.collidepoint(mouse_pos)):
                        self.hover_button = 'restart'
                    elif (hasattr(self, 'details_button') and self.details_button and 
                          self.details_button.collidepoint(mouse_pos)):
                        self.hover_button = 'details'
                    elif (hasattr(self, 'theme_button') and self.theme_button and 
                          self.theme_button.collidepoint(mouse_pos)):
                        self.hover_button = 'theme'
                    elif (hasattr(self, 'quit_button') and self.quit_button and 
                          self.quit_button.collidepoint(mouse_pos)):
                        self.hover_button = 'quit'
                elif self.game_state == "playing":
                    # Handle game theme button hover
                    if (hasattr(self, 'game_theme_button') and self.game_theme_button and 
                        self.game_theme_button.collidepoint(mouse_pos)):
                        self.hover_button = 'game_theme'
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = event.pos
                    
                    if self.game_state == "finished":
                        # Results screen button clicks
                        if (hasattr(self, 'restart_button') and self.restart_button and 
                            self.restart_button.collidepoint(mouse_pos)):
                            self.restart_game()
                        elif (hasattr(self, 'details_button') and self.details_button and 
                              self.details_button.collidepoint(mouse_pos)):
                            self.show_detailed_stats = not self.show_detailed_stats
                        elif (hasattr(self, 'theme_button') and self.theme_button and 
                              self.theme_button.collidepoint(mouse_pos)):
                            self.cycle_theme()
                        elif (hasattr(self, 'quit_button') and self.quit_button and 
                              self.quit_button.collidepoint(mouse_pos)):
                            self.running = False
                    elif self.game_state == "playing":
                        # Game theme button click
                        if (hasattr(self, 'game_theme_button') and self.game_theme_button and 
                            self.game_theme_button.collidepoint(mouse_pos)):
                            self.cycle_theme()
    
    def restart_game(self):
        """Restart the game with fresh state."""
        self.game_state = "playing"
        self.score = 0
        self.wpm = 0
        self.accuracy = 100.0
        self.errors = 0
        self.start_time = None
        self.end_time = None
        self.total_characters_typed = 0
        self.current_result = None
        self.new_sentence()
    
    def wrap_text_for_typing(self, text: str, max_width: int) -> List[str]:
        """Wrap text to fit within typing area, preserving character positions."""
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + (" " if current_line else "") + word
            test_width = self.typing_font.size(test_line)[0]
            
            if test_width <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word
        
        if current_line:
            lines.append(current_line)
        
        return lines
    
    def get_character_position(self, char_index: int, lines: List[str]) -> Tuple[int, int]:
        """Get the screen position (line, position_in_line) for a character index."""
        current_index = 0
        
        for line_num, line in enumerate(lines):
            if current_index + len(line) >= char_index:
                return line_num, char_index - current_index
            current_index += len(line)
            if line_num < len(lines) - 1:  # Add space between lines
                current_index += 1
        
        return len(lines) - 1, len(lines[-1]) if lines else 0
    
    def calculate_stats(self):
        """Calculate WPM and accuracy - fixed to match Monkeytype standards."""
        if self.start_time and self.total_characters_typed > 0:
            elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000.0 / 60.0  # minutes
            if elapsed_time > 0.01:  # Avoid division by very small numbers
                # Monkeytype-style WPM: total characters typed / 5 / minutes
                # This includes all keystrokes (correct + incorrect)
                self.wpm = int((self.total_characters_typed / 5.0) / elapsed_time)
                
                # Cap WPM at reasonable maximum to avoid display issues
                self.wpm = min(self.wpm, 999)
            
            # Accuracy calculation based on total keystrokes vs errors
            if self.total_characters_typed > 0:
                self.accuracy = ((self.total_characters_typed - self.errors) / self.total_characters_typed) * 100
                self.accuracy = max(0, min(100, self.accuracy))  # Clamp between 0-100
    
    def get_wpm_level(self, wpm):
        """Get WPM level and color."""
        if wpm >= 100:
            return "EXPERT", (255, 215, 0)  # Gold
        elif wpm >= 80:
            return "EXCELLENT", (138, 43, 226)  # Purple
        elif wpm >= 60:
            return "BON", (50, 205, 50)  # Green
        elif wpm >= 40:
            return "MOYEN", (255, 165, 0)  # Orange
        elif wpm >= 20:
            return "DÉBUTANT", (135, 206, 235)  # Sky blue
        else:
            return "NOVICE", (255, 99, 71)  # Tomato
    
    def get_accuracy_color(self, accuracy):
        """Get accuracy color based on percentage."""
        if accuracy >= 98:
            return (50, 205, 50)  # Green
        elif accuracy >= 95:
            return (154, 205, 50)  # Yellow-green
        elif accuracy >= 90:
            return (255, 215, 0)  # Gold
        elif accuracy >= 85:
            return (255, 165, 0)  # Orange
        elif accuracy >= 80:
            return (255, 140, 0)  # Dark orange
        else:
            return (255, 99, 71)  # Tomato
    
    def draw_button(self, text, x, y, width, height, is_hovered=False):
        """Draw a clickable button."""
        # Button colors
        bg_color = (60, 60, 60) if not is_hovered else (80, 80, 80)
        border_color = (100, 100, 100) if not is_hovered else self.TEXT_CURRENT
        text_color = self.TEXT_CORRECT if not is_hovered else self.TEXT_CURRENT
        
        # Draw button
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, bg_color, button_rect)
        pygame.draw.rect(self.screen, border_color, button_rect, 2)
        
        # Draw text
        button_text = self.ui_font.render(text, True, text_color)
        text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, text_rect)
        
        return button_rect
    
    def draw_results_screen(self):
        """Draw the professional results screen."""
        self.screen.fill(self.BG_COLOR)
        
        if not self.current_result:
            return
        
        # Title section
        title_y = 40
        title_text = pygame.font.Font(None, 54).render("Résultats de Performance", True, self.TEXT_CORRECT)
        title_rect = title_text.get_rect(center=(self.width // 2, title_y))
        self.screen.blit(title_text, title_rect)
        
        # Warning if not saved
        if not self.game_was_saved:
            warning_text = self.ui_font.render("Session non sauvegardée", True, self.TEXT_INCORRECT)
            warning_rect = warning_text.get_rect(center=(self.width // 2, title_y + 35))
            self.screen.blit(warning_text, warning_rect)
        
        # Main stats section
        main_y = 120 if not self.game_was_saved else 100
        
        # WPM with level
        wpm_level, level_color = self.get_wpm_level(self.current_result['wpm'])
        wpm_large = pygame.font.Font(None, 96).render(str(self.current_result['wpm']), True, level_color)
        wpm_rect = wpm_large.get_rect(center=(self.width // 2, main_y))
        self.screen.blit(wpm_large, wpm_rect)
        
        # WPM label
        wpm_label = pygame.font.Font(None, 32).render("Mots / Minute", True, self.TEXT_INACTIVE)
        wpm_label_rect = wpm_label.get_rect(center=(self.width // 2, main_y + 50))
        self.screen.blit(wpm_label, wpm_label_rect)
        
        # Level badge
        level_text = pygame.font.Font(None, 28).render(f"Niveau: {wpm_level}", True, level_color)
        level_rect = level_text.get_rect(center=(self.width // 2, main_y + 80))
        # Level background
        level_bg = pygame.Rect(level_rect.x - 10, level_rect.y - 5, level_rect.width + 20, level_rect.height + 10)
        pygame.draw.rect(self.screen, (40, 40, 40), level_bg)
        pygame.draw.rect(self.screen, level_color, level_bg, 2)
        self.screen.blit(level_text, level_rect)
        
        # Stats cards section
        cards_y = main_y + 130
        card_width = 180
        card_height = 80
        card_spacing = 20  # Space between cards
        total_cards_width = (3 * card_width) + (2 * card_spacing)
        start_x = (self.width - total_cards_width) // 2
        
        # Accuracy card
        accuracy_color = self.get_accuracy_color(self.current_result['accuracy'])
        accuracy_rect = pygame.Rect(start_x, cards_y, card_width, card_height)
        pygame.draw.rect(self.screen, (40, 40, 40), accuracy_rect)
        pygame.draw.rect(self.screen, accuracy_color, accuracy_rect, 2)
        
        acc_title = pygame.font.Font(None, 24).render("Précision", True, self.TEXT_INACTIVE)
        acc_value = pygame.font.Font(None, 36).render(f"{self.current_result['accuracy']:.1f}%", True, accuracy_color)
        self.screen.blit(acc_title, (start_x + 10, cards_y + 10))
        self.screen.blit(acc_value, (start_x + 10, cards_y + 35))
        
        # Time card  
        time_x = start_x + card_width + card_spacing
        time_rect = pygame.Rect(time_x, cards_y, card_width, card_height)
        pygame.draw.rect(self.screen, (40, 40, 40), time_rect)
        pygame.draw.rect(self.screen, self.TEXT_CURRENT, time_rect, 2)
        
        time_title = pygame.font.Font(None, 24).render("Temps", True, self.TEXT_INACTIVE)
        time_value = pygame.font.Font(None, 36).render(f"{self.current_result['time']:.1f}s", True, self.TEXT_CURRENT)
        self.screen.blit(time_title, (time_x + 10, cards_y + 10))
        self.screen.blit(time_value, (time_x + 10, cards_y + 35))
        
        # Errors card
        error_x = start_x + 2 * (card_width + card_spacing)
        error_color = self.TEXT_CORRECT if self.current_result['errors'] == 0 else self.TEXT_INCORRECT
        error_rect = pygame.Rect(error_x, cards_y, card_width, card_height)
        pygame.draw.rect(self.screen, (40, 40, 40), error_rect)
        pygame.draw.rect(self.screen, error_color, error_rect, 2)
        
        err_title = pygame.font.Font(None, 24).render("Erreurs", True, self.TEXT_INACTIVE)
        err_value = pygame.font.Font(None, 36).render(str(self.current_result['errors']), True, error_color)
        self.screen.blit(err_title, (error_x + 10, cards_y + 10))
        self.screen.blit(err_value, (error_x + 10, cards_y + 35))
        
        # Additional stats (if space allows)
        if self.show_detailed_stats:
            detail_y = cards_y + 110
            details = [
                f"Caractères tapés: {self.current_result['characters_typed']}",
                f"Phrases complétées: {self.current_result['sentences_completed']}/3",
                f"Vitesse moyenne: {self.current_result['characters_typed'] / self.current_result['time']:.1f} car/sec"
            ]
            
            for i, detail in enumerate(details):
                detail_text = self.ui_font.render(detail, True, self.TEXT_INACTIVE)
                detail_rect = detail_text.get_rect(center=(self.width // 2, detail_y + i * 25))
                self.screen.blit(detail_text, detail_rect)
        
        # History graph (smaller) - adjust position to avoid overlap
        if len(self.results_history) > 1:
            graph_y = cards_y + (220 if self.show_detailed_stats else 110)
            self.draw_compact_history_graph(graph_y)
    
    def draw_compact_history_graph(self, y_pos):
        """Draw a smaller, compact version of the history graph."""
        if len(self.results_history) < 2:
            return
        
        # Graph dimensions
        graph_width = self.width - 100
        graph_height = 80
        graph_x = 50
        
        # Background
        pygame.draw.rect(self.screen, (30, 30, 30), (graph_x, y_pos, graph_width, graph_height))
        pygame.draw.rect(self.screen, (60, 60, 60), (graph_x, y_pos, graph_width, graph_height), 1)
        
        # Title
        graph_title = pygame.font.Font(None, 20).render("Progression WPM", True, self.TEXT_INACTIVE)
        title_rect = graph_title.get_rect(center=(self.width // 2, y_pos - 15))
        self.screen.blit(graph_title, title_rect)
        
        # Get recent results
        recent_results = self.results_history[-15:] if len(self.results_history) > 15 else self.results_history
        
        if len(recent_results) < 2:
            return
        
        # Scale calculation
        wpm_values = [r['wpm'] for r in recent_results]
        min_wpm = max(0, min(wpm_values) - 5)
        max_wpm = max(wpm_values) + 5
        wpm_range = max_wpm - min_wpm
        
        if wpm_range == 0:
            return
        
        # Draw points and lines
        points = []
        for i, result in enumerate(recent_results):
            x = graph_x + (i * graph_width // (len(recent_results) - 1))
            y = y_pos + graph_height - int(((result['wpm'] - min_wpm) / wpm_range) * graph_height)
            points.append((x, y))
        
        # Draw line
        if len(points) > 1:
            pygame.draw.lines(self.screen, self.TEXT_CURRENT, False, points, 2)
        
        # Draw points
        for i, point in enumerate(points):
            color = self.TEXT_CORRECT if i == len(points) - 1 else self.TEXT_CURRENT
            pygame.draw.circle(self.screen, color, point, 3)
        
        # Action buttons - adjust position based on content
        base_button_y = self.height - 80
        button_y = base_button_y if not self.show_detailed_stats or len(self.results_history) <= 1 else base_button_y + 20
        button_height = 40
        button_spacing = 20  # Space between buttons
        
        # Calculate individual button widths based on text content
        restart_text = "Rejouer"
        details_text = "Moins" if self.show_detailed_stats else "Plus"
        theme_text = f"Theme: {self.get_theme_name()}"
        quit_text = "Quitter"
        
        restart_width = max(100, self.ui_font.size(restart_text)[0] + 20)
        details_width = max(80, self.ui_font.size(details_text)[0] + 20)
        theme_width = max(120, self.ui_font.size(theme_text)[0] + 20)
        quit_width = max(80, self.ui_font.size(quit_text)[0] + 20)
        
        total_buttons_width = restart_width + details_width + theme_width + quit_width + (3 * button_spacing)
        
        # Center the buttons
        buttons_start_x = (self.width - total_buttons_width) // 2
        
        # Restart button
        restart_x = buttons_start_x
        restart_hovered = self.hover_button == 'restart'
        self.restart_button = self.draw_button(restart_text, restart_x, button_y, restart_width, button_height, restart_hovered)
        
        # Details toggle button
        details_x = restart_x + restart_width + button_spacing
        details_hovered = self.hover_button == 'details'
        self.details_button = self.draw_button(details_text, details_x, button_y, details_width, button_height, details_hovered)
        
        # Theme button
        theme_x = details_x + details_width + button_spacing
        theme_hovered = self.hover_button == 'theme'
        self.theme_button = self.draw_button(theme_text, theme_x, button_y, theme_width, button_height, theme_hovered)
        
        # Quit button
        quit_x = theme_x + theme_width + button_spacing
        quit_hovered = self.hover_button == 'quit'
        self.quit_button = self.draw_button(quit_text, quit_x, button_y, quit_width, button_height, quit_hovered)
    
    def draw_history_graph(self):
        """Draw a line graph of WPM history."""
        if len(self.results_history) < 2:
            return
        
        # Graph area
        graph_x = 100
        graph_y = 420
        graph_width = self.width - 200
        graph_height = 120
        
        # Graph background
        pygame.draw.rect(self.screen, (40, 40, 40), (graph_x, graph_y, graph_width, graph_height))
        pygame.draw.rect(self.screen, self.TEXT_INACTIVE, (graph_x, graph_y, graph_width, graph_height), 1)
        
        # Graph title
        graph_title = self.ui_font.render("Historique WPM (dernières parties)", True, self.TEXT_CORRECT)
        title_rect = graph_title.get_rect(center=(self.width // 2, graph_y - 20))
        self.screen.blit(graph_title, title_rect)
        
        # Get last 20 results for the graph
        recent_results = self.results_history[-20:] if len(self.results_history) > 20 else self.results_history
        
        if len(recent_results) < 2:
            return
        
        # Find min and max WPM for scaling
        wpm_values = [r['wpm'] for r in recent_results]
        min_wpm = max(0, min(wpm_values) - 10)
        max_wpm = max(wpm_values) + 10
        wpm_range = max_wpm - min_wpm
        
        if wpm_range == 0:
            return
        
        # Draw grid lines
        for i in range(5):
            grid_y = graph_y + (i * graph_height // 4)
            pygame.draw.line(self.screen, (60, 60, 60), (graph_x, grid_y), (graph_x + graph_width, grid_y))
            
            # Y-axis labels
            label_wpm = int(max_wpm - (i * wpm_range / 4))
            label_text = pygame.font.Font(None, 16).render(str(label_wpm), True, self.TEXT_INACTIVE)
            self.screen.blit(label_text, (graph_x - 30, grid_y - 8))
        
        # Draw the line graph
        points = []
        for i, result in enumerate(recent_results):
            x = graph_x + (i * graph_width // (len(recent_results) - 1))
            y = graph_y + graph_height - int(((result['wpm'] - min_wpm) / wpm_range) * graph_height)
            points.append((x, y))
        
        # Draw lines between points
        if len(points) > 1:
            pygame.draw.lines(self.screen, self.TEXT_CURRENT, False, points, 2)
        
        # Draw points
        for point in points:
            pygame.draw.circle(self.screen, self.TEXT_CURRENT, point, 3)
        
        # Highlight current game result
        if len(points) > 0:
            pygame.draw.circle(self.screen, self.TEXT_CORRECT, points[-1], 5)
    
    def draw(self):
        """Draw the appropriate screen based on game state."""
        if self.game_state == "finished":
            self.draw_results_screen()
        else:
            self.draw_playing_screen()
        
        pygame.display.flip()
    
    def draw_playing_screen(self):
        """Draw the game screen with Monkeytype-style interface."""
        self.screen.fill(self.BG_COLOR)
        # Update cursor blink animation
        self.cursor_blink_time += self.clock.get_time()
        if self.cursor_blink_time > 530:  # Blink every 530ms
            self.cursor_visible = not self.cursor_visible
            self.cursor_blink_time = 0
        
        # Smooth cursor animation
        if self.cursor_current_x != self.cursor_target_x:
            diff = self.cursor_target_x - self.cursor_current_x
            if abs(diff) < 1:
                self.cursor_current_x = self.cursor_target_x
            else:
                self.cursor_current_x += diff * 0.2  # Smooth interpolation
        
        # Calculate stats
        self.calculate_stats()
        
        # Draw timer and game info
        if self.start_time:
            elapsed = (pygame.time.get_ticks() - self.start_time) / 1000.0
            remaining = max(0, 60 - elapsed)
            timer_text = f"Temps: {remaining:.1f}s"
        else:
            timer_text = "Temps: 60.0s"
        
        # Draw stats at the top
        stats_y = 30
        timer_surface = self.ui_font.render(timer_text, True, self.TEXT_CURRENT)
        wpm_text = self.ui_font.render(f"WPM: {self.wpm}", True, self.TEXT_CURRENT)
        accuracy_text = self.ui_font.render(f"Précision: {self.accuracy:.1f}%", True, self.TEXT_CURRENT)
        score_text = self.ui_font.render(f"Phrases: {self.score}/3", True, self.TEXT_CURRENT)
        # Enhanced debug info
        if self.start_time:
            elapsed_sec = (pygame.time.get_ticks() - self.start_time) / 1000.0
            debug_text = pygame.font.Font(None, 16).render(f"Total: {self.total_characters_typed}, Erreurs: {self.errors}, Temps: {elapsed_sec:.1f}s", True, self.TEXT_INACTIVE)
        else:
            debug_text = pygame.font.Font(None, 16).render(f"Total: {self.total_characters_typed}, Erreurs: {self.errors}, Temps: 0s", True, self.TEXT_INACTIVE)
        
        # Debug: Show sentence completion status
        completion_debug = pygame.font.Font(None, 16).render(f"Tapé: {len(self.typed_text)}/{len(self.current_sentence)} | Match: {self.typed_text == self.current_sentence}", True, self.TEXT_INACTIVE)
        
        self.screen.blit(timer_surface, (50, stats_y))
        self.screen.blit(wpm_text, (200, stats_y))
        self.screen.blit(accuracy_text, (350, stats_y))
        self.screen.blit(score_text, (550, stats_y))
        # Debug info
        self.screen.blit(debug_text, (50, stats_y + 25))
        self.screen.blit(completion_debug, (50, stats_y + 45))
        
        # Typing area
        typing_area_width = self.width - 100
        typing_area_x = 50
        typing_area_y = self.height // 2 - 60
        
        # Wrap text for display
        lines = self.wrap_text_for_typing(self.current_sentence, typing_area_width)
        line_height = self.typing_font.get_height() + 10
        
        # Draw each character with appropriate color and update cursor position
        sentence_char_index = 0  # Index in the original sentence
        cursor_line_y = typing_area_y  # Track cursor Y position
        cursor_found = False
        
        for line_num, line in enumerate(lines):
            line_y = typing_area_y + (line_num * line_height)
            current_x = typing_area_x
            
            for char_pos, char in enumerate(line):
                char_color = self.TEXT_INACTIVE  # Default: untyped (gray)
                display_char = char  # Character to display
                
                if sentence_char_index < len(self.typed_text):
                    # This character has been typed
                    typed_char = self.typed_text[sentence_char_index]
                    if typed_char == char:
                        char_color = self.TEXT_CORRECT  # Correct (white)
                    else:
                        char_color = self.TEXT_INCORRECT  # Incorrect (red)
                        # SPECIAL CASE: Show incorrect character when expected char is space
                        if char == ' ':
                            display_char = typed_char  # Show what was actually typed instead of space
                            # Draw background highlight to make it more visible
                            highlight_rect = pygame.Rect(current_x, line_y, self.typing_font.size(typed_char)[0], self.typing_font.get_height())
                            pygame.draw.rect(self.screen, (80, 20, 20), highlight_rect)  # Dark red background
                elif sentence_char_index == len(self.typed_text) and not cursor_found:
                    # This is the current character to type
                    char_color = self.TEXT_CURRENT  # Current (yellow)
                    # Update target cursor position ONLY ONCE
                    self.cursor_target_x = current_x
                    cursor_line_y = line_y
                    cursor_found = True
                
                # Render and draw the character
                char_surface = self.typing_font.render(display_char, True, char_color)
                self.screen.blit(char_surface, (current_x, line_y))
                
                current_x += char_surface.get_width()
                sentence_char_index += 1
            
            # Add space character between lines (except for last line)
            if line_num < len(lines) - 1 and sentence_char_index < len(self.current_sentence):
                # Handle the space character that was split between lines
                if sentence_char_index < len(self.typed_text):
                    # Space was typed
                    typed_char = self.typed_text[sentence_char_index]
                    expected_char = self.current_sentence[sentence_char_index]
                    if typed_char != expected_char:
                        # ERROR: Wrong character typed instead of space between lines
                        # Show the incorrect character at the start of next line with highlight
                        next_line_y = typing_area_y + ((line_num + 1) * line_height)
                        error_surface = self.typing_font.render(typed_char, True, self.TEXT_INCORRECT)
                        highlight_rect = pygame.Rect(typing_area_x - 20, next_line_y, error_surface.get_width() + 4, self.typing_font.get_height())
                        pygame.draw.rect(self.screen, (80, 20, 20), highlight_rect)  # Dark red background
                        pygame.draw.rect(self.screen, self.TEXT_INCORRECT, highlight_rect, 2)  # Red border
                        self.screen.blit(error_surface, (typing_area_x - 18, next_line_y))
                elif sentence_char_index == len(self.typed_text) and not cursor_found:
                    # Cursor should be at the space position (start of next line)
                    self.cursor_target_x = typing_area_x  # Start of next line
                    cursor_line_y = typing_area_y + ((line_num + 1) * line_height)
                    cursor_found = True
                
                sentence_char_index += 1
        
        # Handle special case: cursor at end of sentence
        if not cursor_found and len(self.typed_text) >= len(self.current_sentence):
            # Position cursor at the end of the last line
            if lines:
                last_line_num = len(lines) - 1
                last_line_y = typing_area_y + (last_line_num * line_height)
                last_line_width = self.typing_font.size(lines[last_line_num])[0]
                self.cursor_target_x = typing_area_x + last_line_width
                cursor_line_y = last_line_y
        
        # Draw animated cursor
        if self.cursor_visible:
            cursor_height = self.typing_font.get_height()
            # Use animated position for smooth movement
            animated_cursor_x = self.cursor_current_x
            pygame.draw.line(self.screen, self.CURSOR_COLOR, 
                           (animated_cursor_x, cursor_line_y), 
                           (animated_cursor_x, cursor_line_y + cursor_height), 2)
        
        # Draw instructions at bottom
        instructions = [
            "Tapez le texte affiché ci-dessus | ESC pour terminer",
            f"Mots chargés: {len(self.words):,}"
        ]
        
        y_offset = self.height - 80
        for instruction in instructions:
            inst_text = self.ui_font.render(instruction, True, self.TEXT_INACTIVE)
            inst_rect = inst_text.get_rect(center=(self.width // 2, y_offset))
            self.screen.blit(inst_text, inst_rect)
            y_offset += 25
        
        # Add theme button in bottom-right corner
        theme_button_text = f"Theme: {self.get_theme_name()}"
        theme_button_width = max(120, self.ui_font.size(theme_button_text)[0] + 20)
        theme_button_height = 30
        theme_button_x = self.width - theme_button_width - 20
        theme_button_y = self.height - theme_button_height - 20
        theme_hovered = self.hover_button == 'game_theme'
        self.game_theme_button = self.draw_button(theme_button_text, 
                                                 theme_button_x, theme_button_y, 
                                                 theme_button_width, theme_button_height, 
                                                 theme_hovered)
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)  # 60 FPS