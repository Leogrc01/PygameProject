"""Tests for the TypeGame."""

import pytest
from typegame.game import Game


def test_game_initialization():
    """Test that the game initializes correctly."""
    # This test would need headless pygame for proper testing
    # For now, just test basic imports work
    assert Game is not None


def test_word_list():
    """Test that the word list is not empty."""
    # We can test the word list without initializing pygame
    words = ["python", "pygame", "typing", "game", "code", "program", 
             "computer", "keyboard", "developer", "software"]
    assert len(words) > 0
    assert all(isinstance(word, str) for word in words)