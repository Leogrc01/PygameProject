# TypeGame

A Python-based typing game built with Pygame.

## Setup

1. Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python -m typegame
```

## Development

Install development dependencies:
```bash
pip install -e ".[dev]"
```

Run tests:
```bash
pytest
```

Format code:
```bash
black .
```

## Project Structure

- `typegame/` - Main game package
- `assets/` - Game assets (images, sounds)
- `tests/` - Unit tests
- `src/` - Additional source files if needed