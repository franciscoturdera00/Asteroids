# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build & Run Commands

```bash
# Install dependencies
python -m pip install -r requirements.txt

# Run the game (default: 1400x900)
python main.py

# Run with custom screen dimensions
python main.py --width 1920 --height 1080

# Create executable (requires copying Sounds/ and Fonts/ to dist/main/)
pyinstaller main.py
```

**Requirements:** Python 3.10+, pygame, pyinstaller (for builds)

## Project Structure

```
Asteroids/
├── main.py                          # Entry point, pygame init, CLI args
├── requirements.txt                 # Dependencies (pygame, pyinstaller)
├── game_logic/                      # Core game controllers
│   ├── Game.py                      # Main game loop orchestrator
│   ├── PreGame.py                   # Mode selection menu (1P/2P)
│   ├── Score.py                     # Score tracking with decay
│   └── Lives.py                     # Per-player lives management
├── Interactables_Objects/           # Entity classes
│   ├── Player.py                    # Player controls & physics
│   ├── Asteroid.py                  # Procedural asteroids with gravity
│   ├── Bullet.py                    # Projectiles with lifetime
│   ├── Alien.py                     # AI enemy behavior
│   └── Items/                       # Powerup system
│       ├── Item.py                  # Abstract base class
│       ├── PlusBulletItem.py        # +1 max bullets
│       ├── BlackHoleItem.py         # Area destruction effect
│       └── ExtraLifeItem.py         # Life/revive pickup
├── Fonts/                           # TTF/OTF font files
├── Sounds/                          # WAV audio assets (13 files)
└── Images/                          # Reference sprites (PNG/JPG)
```

## Architecture

This is a Pygame-based Asteroids recreation with single and multiplayer support.

### Game Flow

```
main.py → PreGame (menu) → Game (main loop) → Post-game → Back to PreGame
```

### Core Classes

| Class | File | Purpose |
|-------|------|---------|
| `Game` | `game_logic/Game.py` | Main controller: spawning, collisions, state management, rendering |
| `PreGame` | `game_logic/PreGame.py` | Menu screen for 1P/2P mode selection |
| `Score` | `game_logic/Score.py` | Score tracking with time decay and event bonuses |
| `Lives` | `game_logic/Lives.py` | Per-player lives with UI rendering |
| `Player` | `Interactables_Objects/Player.py` | Player physics, input, bullets, invincibility |
| `Asteroid` | `Interactables_Objects/Asteroid.py` | Three sizes, procedural vertices, gravity pull |
| `Bullet` | `Interactables_Objects/Bullet.py` | 5-second lifetime projectiles |
| `Alien` | `Interactables_Objects/Alien.py` | AI with goal-seeking movement |
| `Item` | `Items/Item.py` | Abstract base class for powerups |

### Class Relationships

- **Game** orchestrates all entities (Players, Asteroids, Aliens, Items, Score)
- **Player** owns its Bullets list and associated Lives instance
- **Item** is an abstract base class; PlusBulletItem, BlackHoleItem, ExtraLifeItem inherit from it

## Key Constants

### Game Settings (Game.py)
- FPS: 45
- Background asteroids: 300 (aesthetic only)
- Initial asteroids: 7
- Initial player lives: 3
- Item spawn rate: 20% (asteroids), 60% (aliens)

### Player Settings (Player.py)
- Acceleration: 0.075/frame
- Max speed: 5 px/frame
- Invincibility duration: 2 seconds post-spawn
- Max bullets: 3 (upgradeable)
- Hitbox radius: 18 × scale

### Asteroid Settings (Asteroid.py)
- Sizes: LARGE (60), MEDIUM (40), SMALL (15)
- Speed range: 0.3-1.0 px/frame
- Gravitational constant: 1e-7

### Scoring (Score.py)
- Initial score: 500
- Decay: -1 every 75 frames
- Asteroid hit: +50 to +3000 (size dependent)
- Alien hit: +2000
- Bullet fired: -50
- Player hit: -700
- Win bonus: +100000 × remaining lives

## Controls

| Action | Player 1 | Player 2 |
|--------|----------|----------|
| Thrust | W | I |
| Rotate Left | A | J |
| Rotate Right | D | L |
| Shoot | SPACE | R_SHIFT |

## Code Conventions

### Design Patterns Used
- **Abstract Base Class**: Item with `@abstractmethod render()` and `@final perform_action()`
- **Template Method**: Item subclasses override `perform_action_on_*` methods
- **Factory Pattern**: Weighted random item creation in `Game._spawn_item_with_chance()`

### Naming Conventions
- Private methods: prefixed with `_` (e.g., `_player_collision_detected()`)
- Descriptive method names: `_handle_bullet_collisions()`, `_update_asteroids()`
- Constants: UPPER_SNAKE_CASE (e.g., `LARGE`, `MEDIUM`, `SMALL`)

### Type Hints
- Uses Python 3.10+ union syntax (`|`) for optional types
- Generic types from typing module: `List[T]`, `TypeVar`, `Union`, `Tuple`
- Forward references for circular dependencies

### Pygame Patterns
- Positions use `pygame.Vector2`
- Rendering via `draw.polygon()`, `draw.circle()`, `draw.line()`
- Screen wrapping: `position % screen_dimension`
- Angles stored in degrees, converted to radians for math operations

## Key Mechanics

### Physics
- Velocity-based movement with acceleration
- Screen edge wrapping (entities appear on opposite side)
- Asteroids have gravitational pull toward players

### Collision Detection
- Distance-based using `distance_to()` method
- Each entity type has defined hitbox radius
- Handled centrally in `Game._handle_*_collisions()` methods

### Item System
- Items spawn on entity destruction with weighted random selection
- 15-second lifetime with blinking effect near expiration
- Items have directional movement and screen wrapping

## Assets

### Sounds (13 WAV files)
- Background music, explosions (3 sizes), fire, thrust
- Alien hit, item pickups (life, bullet, blackhole), win/lose

### Fonts (3 files)
- `novem.ttf` - Primary game font
- `ARCADECLASSIC.TTF` - Classic arcade style
- `wheaton_capitals.otf` - Title/decorative

## Development Notes

- Most entity classes have a `debug` mode flag for visualization
- Game loop runs at 45 FPS via `Clock.tick()`
- Sound playback uses `pygame.mixer` with Channels for concurrent audio
- Invincibility frames count down each update cycle
