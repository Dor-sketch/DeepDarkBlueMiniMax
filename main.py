"""
Main file to run the GUI for the TicTacToe game.
Player can choose to switch to the stone game from the GUI.
"""
import tkinter as tk
from gui import TicTacToeGUI
from game import TicTacToe
from minimax import Minimax


def main():
    """
    Run the StoneGameGUI
    """
    root = tk.Tk()
    game_logic = Minimax(TicTacToe())
    game = TicTacToeGUI(root, game_logic)
    root.mainloop()


if __name__ == "__main__":
    main()
