# RuneScape Adventure
This is a simple text-based game where you can fight goblins, buy items, and train to level up.

## Prerequisites
- Python 3.x
- colorama module (install using pip install colorama)

## How to play
- Clone the repository or download the runescape_adventure.py file
- Open your terminal or command prompt and navigate to the directory where the file is located
- Run the command python game.py to start the game
- Follow the on-screen instructions to play the game

## Game Mechanics
### Player
- Name: Player's name
- Health: Starting health is 100. Decreases when the player is attacked by enemies.
- Attack: Starting attack power is 10. Increases when the player levels up.
- Defense: Starting defense power is 5. Decreases the damage taken from enemy attacks.
- Level: Starting level is 1. Increases when the player gains enough experience points.
- Experience: Starting experience points is 0. Increases when the player defeats enemies or trains.
- Gold: Starting gold is 0. Can be obtained by defeating enemies or training.
- Woodcutting: Spend your gold that you earned to level up
- Save state: The game keeps a savestate now

### Enemies
- Name: Goblin
- Health: Starting health is 50.
- Attack: Starting attack power is 5.
- Defense: Starting defense power is 2.
- Level: Starting level is 1.

## Actions
- Fight goblins: Fight goblins to gain experience points and gold. If the player defeats the goblin, they gain 10 gold and experience points equal to the goblin's level times 10. If the player's health reaches 0, the game is over.
- View status: View the player's current status, including name, health, attack, defense, level, experience points, and gold.
- Buy item: Buy an item for 20 gold. If the player has enough gold, they can buy the item and reduce their gold by 20. If they do not have enough gold, they cannot buy the item.
- Train: Train to gain experience points and gold. If the player is at least level 2, they can choose to train and gain experience points and gold. The number of times they train is based on the user input. Each training session takes 5 seconds. If the player gains enough experience points, they will level up and gain more health, attack, defense, and gold. If they do not gain enough experience points, they will gain 20 experience points and gold based on their level.
- Quit game: Quit the game.

## Credits
- This game was created by The XSS Rat.
