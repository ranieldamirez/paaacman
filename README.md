# PACCCMAN 

## Project Overview

This project is a Pac-Man-inspired arcade game where the player controls a character navigating a maze to collect items (dots), avoid enemies (ghosts), and clear each level. The game includes:

- A **start menu** to begin the game.
- A **main game screen** for gameplay.
- A **game-over screen** upon losing.
- **High-score tracking** and user data storage.

### Core Features:
1. **Player Movement**: Navigate the maze using keyboard inputs.
2. **Enemy Bots**: Ghosts with dynamic behaviors that challenge the player.
3. **Collision Detection**: Determine interactions between the player, enemies, and items.
4. **Scoring System**: Points for collecting dots and defeating enemies.
5. **Level Progression**: Advance to the next level after clearing the maze.

---

## Design Patterns

### 1. **Singleton Pattern**
- **Purpose**: Centralized management of game states and high-score tracking.
- **Usage**: Ensures a single instance of the game manager exists throughout gameplay.

### 2. **Observer Pattern**
- **Purpose**: Real-time updates to game elements based on player actions or events.
- **Usage**: Synchronizes changes like score updates or player lives after collisions.

### 3. **Strategy Pattern**
- **Purpose**: Modular and interchangeable behaviors for enemy bots.
- **Usage**: Handles ghost behaviors such as:
  - Random movement.
  - Chasing the player.
  - Defensive patterns.

### 4. **Decorator Pattern**
- **Purpose**: Add dynamic abilities or power-ups during gameplay.
- **Usage**: Enables features like:
  - Temporary speed boosts.
  - Freezing enemies.
  - Shielding from collisions.

---

## Technology Stack

- **Language**: Python
- **Framework**: Pygame Library (simplifies 2D game development).

**Alternative Option**: Java with JavaFX (if desired for enhanced user interface capabilities).

---

## File Structure

- `game.py`: Main entry point of the game.
- Additional files: For modular handling of player movement, enemy behaviors, scoring system, and UI components.

---

## How to Run

1. Install Python 3.x and the Pygame library:
   ```bash
   pip install pygame
   ```
2. Clone this repository:
   ```bash
   git clone <https://github.com/ranieldamirez/pacccman.git>
   ```
3. Navigate to the project > 'code' folder and start the game:
   ```bash
   python game.py
   ```

---

## Future Improvements

- Enhanced AI for enemy behaviors.
- More levels with increasing complexity.
- Additional power-ups for strategic gameplay.
- Multiplayer mode for cooperative or competitive play.

--- 

Enjoy the game! 😊
