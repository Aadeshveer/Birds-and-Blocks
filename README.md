# Birds and Blocks

A 2-Player, turn-based, physics-driven catapult game inspired by Angry Birds, built with Pygame for CS 104 at IIT Bombay (2024-25). Features custom physics, unique bird abilities, destructible environments, a strategic upgrade system, persistent ELO ratings with a leaderboard, and all-original pixel art.

**Author:** Aadeshveer Singh (24B0926)

---

## Core Features & Customizations

*   **2-Player Turn-Based Gameplay:** Compete to demolish the opponent's fortress.
*   **Custom Physics Engine:** Realistic gravity-based projectile motion.
*   **Mouse-Controlled Launching:** Drag and pull to aim and set power.
*   **Diverse Projectiles & Blocks:**
    *   Birds: Red (Balanced), Chuck (vs. Wood), Blues (vs. Glass), Bomb (vs. Stone) – each with unique, upgradable abilities.
    *   Blocks: Wood, Stone, Glass – distinct health and 5-stage visual damage.
*   **Strategic Card & Upgrade System:** Choose bird cards and upgrade their abilities.
*   **Persistent ELO Rating System & Leaderboard:** Track player skill with ELO ratings stored between sessions and displayed on a leaderboard.
*   **Full UI & Dynamic Tutorial:** Main Menu, Player Name Entry (with ELO display), Gameplay, Game Over, Leaderboard, and context-aware tutorial overlays.
*   **All-Original Custom Assets:** All visual assets (birds, blocks, UI, animations) and the game font were created pixel-by-pixel by the author using Aseprite.
*   **Advanced Particle System & Dynamic Camera:** Enhancing visual feedback and gameplay focus.
*   **Custom Sound Effects & Music.**

---

## Setup & Running

1.  **Prerequisites:** Python 3.x, Pygame Community Edition (pygame-ce).
2.  **Clone:**
    ```bash
    git clone https://github.com/your-username/birds-and-blocks.git # Replace with your repo URL
    cd birds-and-blocks
    ```
3.  **Install Pygame-CE:**
    ```bash
    pip install pygame-ce
    ```
4.  **Run (from source):**
    ```bash
    python main.py
    ```
    *(A pre-compiled Windows executable `Birds_and_blocks(windows).exe` may also be available, ensure `assets/` and `user_data/` are in the same directory.)*

---

## Project Structure

*   `main.py`: Game entry point.
*   `scripts/`: Modules for birds, blocks, cards, player logic, UI modes, particles, ELO ratings, and utilities.
*   `assets/`: Holds all images, sounds, and the custom font.
*   `user_data/`: Stores persistent player names and ELO ratings.

---

**This project fulfills all basic requirements and implements several advanced features. For a comprehensive breakdown of game mechanics, implementation details, physics, asset creation, ELO system, and the project journey, please refer to the detailed LaTeX project report (`report/report.pdf`).**
