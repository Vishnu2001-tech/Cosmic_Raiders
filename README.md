# Space Invaders Game

A classic Space Invaders game implemented in Python using Pygame with retro arcade styling.

## Features

- **Retro Arcade UI**: Custom pixel-style font system with fallback support
- **Main Menu**: Navigate with arrow keys, authentic arcade experience
- **Player spaceship** that moves left and right
- **Shooting mechanics** with bullet cooldown
- **Grid formation** of alien enemies
- **Smart alien movement**: Move horizontally and descend when hitting edges
- **Alien AI**: Aliens shoot back randomly
- **Collision detection** for all interactions
- **Score tracking** and lives system with high score persistence
- **Wave system**: Progressive difficulty with new waves
- **Game over conditions** with restart functionality
- **60 FPS optimized** performance
- **Multiple game states**: Menu, Playing, Game Over

## Controls

### Main Menu
- **Arrow Keys**: Navigate menu options
- **Enter/Space**: Select menu option
- **ESC**: Quit game

### Gameplay
- **Arrow Keys** or **A/D**: Move left and right
- **Spacebar**: Shoot bullets
- **ESC**: Return to main menu

### Game Over
- **R**: Restart game
- **ESC**: Return to main menu

## Installation

1. Install Python 3.6 or higher
2. Install Pygame:
   ```bash
   pip install -r requirements.txt
   ```
   or
   ```bash
   pip install pygame
   ```

3. **Optional - Add Pixel Font for Retro Look**:
   - Download a pixel-style font (like "Pixeled.ttf" or "Press Start 2P")
   - Place it as `fonts/Pixeled.ttf`
   - Game will automatically use it for authentic arcade styling
   - Falls back to system font if not available

## Running the Game

```bash
python3 space_invaders.py
```

## Game Rules

- Start with 3 lives
- Destroy aliens to earn 10 points each
- Avoid alien bullets and prevent aliens from reaching the bottom
- Game ends when you run out of lives or aliens reach your position
- New wave of aliens spawns after clearing all enemies
- High scores are tracked across sessions

## Font System

The game uses a 4-tier font system for authentic arcade styling:

- **Title (48px)**: Main menu title "SPACE INVADERS"
- **Large (32px)**: Score display, menu options
- **Medium (24px)**: Subtitles, wave counter, instructions
- **Small (16px)**: Detailed instructions and hints

## Technical Details

- Runs at 60 FPS for smooth gameplay
- Optimized collision detection using pygame.Rect
- Memory efficient bullet management (removes off-screen bullets)
- Configurable game parameters in constants section
- Modular font management system with fallback support
- State-based game architecture (Menu → Playing → Game Over)

## File Structure

```
space_invaders.py       # Main game file
requirements.txt        # Python dependencies
fonts/                  # Font directory
├── Pixeled.ttf        # Custom pixel font (optional)
└── README.md          # Font setup instructions
```
