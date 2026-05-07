# AI Grid Survival Game

Welcome to the AI Grid Survival Game! This is a simple, real-time 2D grid survival game built with Python and `pygame-ce`. In this game, your goal is to survive as long as possible by scavenging for resources while avoiding hostile AI entities that aggressively hunt you down.

## Prerequisites

- **Python 3.8+** must be installed on your machine.
- You must install the game dependencies before running.

## Installation and Running

1. **Install dependencies:**
   Open your terminal in the project directory and run:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Game:**
   Start the game with:
   ```bash
   python main.py
   ```

## Controls

The game is played in a single window and controlled entirely through the keyboard.

- **Movement:** Use the **Arrow Keys** (UP, DOWN, LEFT, RIGHT) or **W, A, S, D** to navigate the player across the grid.
- **Restart Game:** If you die and hit the Game Over screen, press the **R** key to restart the game instantly.

## The Entities

- **Electric Blue Square (You):** This is your character. Keep moving to stay alive!
- **Gold Square (Food):** Restores your **Hunger** by 20 points and awards 10 points to your score. 
- **Green Square (Health Pack):** Restores your **Health** by 10 points and awards 10 points to your score.
- **Red Square (Enemy):** These hostile entities continuously scan the grid for your location and ruthlessly pursue you. Touching them deals 20 damage! They will also **engulf** nearby gold squares to **increase in number**, splitting into two entities whenever they feast.

## Game Rules and Mechanics

1. **Hunger Depletion:** Your character's hunger starts at 100 and naturally depletes by 1 point every second as you burn energy.
2. **Starvation:** If your hunger hits 0, you begin to starve and will lose 5 health points every second. Keep eating food (gold squares) to prevent starvation!
3. **Enemy Spawning & Multiplication:** Enemies spawn every 3 seconds at a random edge of the screen. Additionally, if an enemy reaches a gold square (food), it will consume it and split, creating a new enemy at its location.
4. **Scoring:** The goal is to accumulate the highest score possible. You are awarded 10 points for every piece of food or health pack you pick up.
5. **Game Over:** If your Health reaches 0, you die and the game is over. Your final score will be displayed on the screen.

Good luck! Have fun surviving the grid!
