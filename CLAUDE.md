# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Run Commands

```bash
# Install dependencies
python -m pip install -r requirements.txt

# Run the game
python main.py

# Run with custom screen dimensions
python main.py --width 1920 --height 1080

# Create executable (requires copying Sounds/ and Fonts/ to dist/main/)
pyinstaller main.py
```

## Architecture

This is a Pygame-based Asteroids recreation with single and multiplayer support.

### Core Structure

- **`main.py`** - Entry point; initializes pygame, parses screen dimension args, starts game loop
- **`game_logic/Game.py`** - Main game controller orchestrating all gameplay (spawning, collisions, state management)
- **`game_logic/PreGame.py`** - Menu screen for mode selection (1P/2P)
- **`game_logic/Score.py`** - Score tracking with time decay and event bonuses/penalties
- **`game_logic/Lives.py`** - Per-player lives management with UI rendering

### Entity System (`Interactables_Objects/`)

- **`Player.py`** - Player controls, physics (acceleration, max speed), bullet management, invincibility frames
- **`Asteroid.py`** - Three sizes (LARGE/MEDIUM/SMALL), procedural shape generation, gravitational pull toward players, fragments on destruction
- **`Alien.py`** - AI enemy with interval-based movement toward player positions
- **`Bullet.py`** - Projectiles with 5-second lifetime and screen wrapping

### Item System (`Interactables_Objects/Items/`)

Items spawn randomly when asteroids/aliens are destroyed. Base class `Item.py` provides common behavior (15-second lifetime, blinking effect).

- **`PlusBulletItem.py`** - Increases player's max bullets
- **`BlackHoleItem.py`** - Creates expanding destruction zone (500px radius)
- **`ExtraLifeItem.py`** - Adds life or revives dead player in multiplayer

### Key Mechanics

- **Physics**: Velocity-based movement with acceleration, screen edge wrapping, gravity affecting asteroid trajectories
- **Collision**: Game.py handles all collision detection between entities
- **Multiplayer Controls**: Player 1 uses W/A/D/SPACE, Player 2 uses I/J/L/R_SHIFT
- **Scoring**: Starts at 500, decays over time, rewards hits (+50-2000), penalizes shots fired (-50) and damage taken (-700)
