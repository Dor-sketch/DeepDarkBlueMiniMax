# Stone Taking Game

A simple yet engaging game where you compete against the computer in taking stones from a pile. The game is a fun mix of strategy and luck, designed to provide an entertaining challenge. It employs a graphical user interface (GUI) for interaction and visualizes the game strategy using a minimax algorithm tree.

This game was originally presented in the hard leetcode problem [https://leetcode.com/problems/stone-game-iii/](https://leetcode.com/problems/stone-game-iii/). This implementation is not applicable to the leetcode problem, but it is a fun game to play. Its purpose is to demonstrate the minimax algorithm and provide an interactive experience for players, while also offering insight into the game's decision-making process and the alpha-beta pruning algorithm.

## Features

- **Player vs. Computer Gameplay**: Take turns with the computer to remove 1-3 stones from the pile.
- **Minimax Algorithm**: The computer calculates its moves using the minimax algorithm, ensuring a challenging game.
- **GUI Interaction**: The game uses Tkinter for the GUI, making it interactive and user-friendly.
- **Visualization**: Utilizes NetworkX for visualizing the minimax strategy tree, offering insight into the game's decision-making process.
- **Dynamic Stone Pile**: The number of stones and their values in the pile can be randomized for each game, ensuring a unique experience every time.

## Prerequisites

Before running the game, ensure you have the following installed:

- Python 3.x
- Tkinter
- NetworkX
- Matplotlib
- PyDot (for tree visualization)

## How to Run

1. Clone the repository or download the game file.
2. Ensure you have all the necessary libraries installed.
3. Run the script using Python:

```bash
pythons minigame.py
```

## Game Play

1. **Starting the Game**: Upon launching, the game will display a pile of stones with randomized values.
2. **Making a Move**: Enter the number of stones you wish to take (1, 2, or 3) and click "Take Stones".
3. **Computer's Turn**: After your move, the computer will calculate its best move and take stones accordingly.
4. **Visualization**: Click "Show Tree" to visualize the minimax decision tree for the current state of the game.
5. **End of Game**: The game ends when there are no more stones to take. The player with the most stones wins.

## Strategy

The key to winning is to anticipate the computer's moves and strategize accordingly. Since the computer uses the minimax algorithm, it will try to minimize your potential gain while maximizing its own. Try different strategies and see how the computer responds to sharpen your game plan.

## Customization

Feel free to modify the initial number of stones or their values in the `main` function to customize your gaming experience.

## Feedback

We love to hear from players! If you have any feedback, suggestions, or issues, please open an issue in the repository.

Enjoy the game and may the best strategist win!
