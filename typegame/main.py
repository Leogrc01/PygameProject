"""Main entry point for the TypeGame."""

import pygame
import sys
from .game import Game


def main():
    """Run the typing game."""
    pygame.init()
    
    try:
        game = Game()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    main()