# Nexus-Rover
Nexus Rover is an intelligent automation script designed for the game Poke Nexus.


Nexus Rover v1.2.0
Nexus Rover is an intelligent automation script designed for the game Poke Nexus. It utilizes advanced Computer Vision (CV) to navigate cities, avoid obstacles, and efficiently farm experience points and items in any grassy area.

Key Features

Dynamic Location Detection: Automatically detects your current location (e.g., after exiting a PokeCenter) and executes a pre-programmed path back to the farming zone.
Intelligent Grass Scanning: The Rover doesn't move blindly. It scans the surroundings within a 110-unit radius and moves only when it detects a grass tile.
Universal Grass Support: Compatible with all types of grass textures—once the bot enters a grassy area, it automatically switches to "Hunting Mode."
Advanced Combat System:
Auto-Menu Opening: Uses a "Double-Tap" logic for 100% reliability when opening the fight menu.
Random Skill Selection: Randomly chooses moves (1-4) to simulate human behavior and prevent repetitive patterns.
Hard Key Reset: Automatically releases all virtual keys to prevent the character from getting stuck after long walks.
Anti-Lag Integration: Built-in synchronization pauses tailored for server-side delays and UI animations.

Supported Locations (Maps)

Currently, the script features precise navigation paths for:
Cerulean City – Full route from the PokeCenter to the deep grass fields in the North/West.
Celadon City – Automatic exit towards the Eastern routes.
Pro Tip: The bot can support any new city. Simply add a screenshot of the location name to data/maps and define the movement sequence in the script.

How It Works

Detection: The script captures the Poke Nexus game window using the mss library.
Analysis: Using OpenCV, it compares the captured frame against templates stored in data/img/ (fight icons, grass textures, city headers).
Action: Based on the detected state (Combat / City / Exploration), the pydirectinput library sends direct hardware-level signals to the game engine.

Requirements

Python 3.10+
Dependencies: opencv-python, numpy, mss, pygetwindow, pydirectinput.
Display: Game must be running in Windowed Mode.

Installation & Usage

Clone the repository or download the start.py file.
Install the required libraries:
pip install opencv-python numpy mss pygetwindow pydirectinput

Ensure your data/img and data/maps folders contain the necessary .jpg templates.

Run the bot:
python start.py

Author's Note

The bot is under continuous development. Version 1.2.0 focuses on combat system stability and navigation precision in Cerulean City. Use responsibly and respect the game's community guidelines.
Would you like me to add a "Troubleshooting" section to this README to explain how to fix the "entering backpack/pokemon menu" issue if it happens again?
