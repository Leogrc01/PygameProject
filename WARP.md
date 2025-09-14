# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

TypeGame is a Python-based typing game built with Pygame. It's a simple educational game where players type words displayed on screen to improve their typing skills.

## Development Commands

### Environment Setup
```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies for development
pip install -e ".[dev]"
```

### Running the Game
```bash
# Run as module (preferred method)
python -m typegame

# Alternative: direct execution
python typegame/main.py
```

### Testing
```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_game.py

# Run with verbose output
pytest -v

# Run single test function
pytest tests/test_game.py::test_game_initialization
```

### Code Quality
```bash
# Format code with Black
black .

# Check formatting without making changes
black --check .

# Lint with flake8
flake8 typegame/ tests/

# Format specific file
black typegame/game.py
```

### Package Management
```bash
# Install production dependencies only
pip install -r requirements.txt

# Install as editable package with dev dependencies
pip install -e ".[dev]"

# Update requirements after adding dependencies
pip freeze > requirements.txt
```

## Architecture Overview

### Core Structure
- **`typegame/`** - Main game package containing all game logic
- **`tests/`** - Unit tests (currently minimal, suitable for expansion)
- **`assets/`** - Directory mentioned in README but not yet present (for future game assets)

### Key Components

**Game Entry Points:**
- `typegame/__main__.py` - Enables `python -m typegame` execution
- `typegame/main.py` - Main entry point with error handling and pygame lifecycle
- Console script defined in `pyproject.toml` creates `typegame` command

**Core Game Logic:**
- `typegame/game.py` - Contains the main `Game` class with all game mechanics:
  - Event handling (keyboard input, quit events)
  - Word generation and validation
  - Score tracking
  - Rendering (text, colors, layout)
  - 60 FPS game loop

### Game Features
- Random word selection from predefined list
- Real-time typing feedback with color coding (green for correct, red for incorrect)
- Score tracking based on completed words
- Simple keyboard controls (ESC to quit, backspace support)
- Clean pygame-based UI with centered text layout

## Development Patterns

### Code Style
- Black formatting with 88-character line length
- Type hints used in function signatures
- Docstrings for classes and methods
- Python 3.8+ compatibility

### Testing Strategy
- Pytest framework configured in `pyproject.toml`
- Tests currently minimal due to pygame's graphical nature
- Room for expansion with headless testing or mocking

### Dependencies
- **pygame** - Core graphics and input handling
- **numpy** - Mathematical operations (though not heavily used currently)
- **pytest** - Testing framework
- **black** - Code formatting
- **flake8** - Code linting

## Common Development Tasks

### Adding New Words
Words are currently hardcoded in `game.py`. To add new words, modify the `self.words` list in the `Game.__init__` method.

### Modifying Game Mechanics
Core game logic is centralized in the `Game` class. Key methods:
- `handle_events()` - Input processing
- `draw()` - Rendering
- `new_word()` - Word generation
- `run()` - Main game loop

### Pygame Development Notes
- Game requires pygame initialization before creating Game instances
- All pygame operations should be wrapped in try/except blocks
- Always call `pygame.quit()` on exit to prevent resource leaks
- Uses 60 FPS with `clock.tick(60)`

### Testing Considerations
Testing pygame applications requires special handling:
- Direct pygame testing needs headless mode or display mocking
- Focus tests on game logic rather than rendering
- Consider separating business logic from pygame-specific code for better testability