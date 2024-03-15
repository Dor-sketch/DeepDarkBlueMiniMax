"""
This module contains the GUI for the StoneGame and TicTacToe games.
"""

import random
from tkinter import messagebox
import tkinter as tk
from minimax import Minimax
from game_tree import GameTree
from game_tic_tac_toe import TicTacToe
from game_stone_game import StoneGame


class GameGUI:
    """
    StoneGameGUI class
    """

    def __init__(self, root, minimax):
        self.root = root
        self.minimax = minimax
        self.root.title("My Game")
        self.root.geometry("400x400")
        self.canvas = tk.Canvas(self.root, width=300,
                                height=300, bg='light blue')
        self.frame = tk.Frame(self.root)
        self.frame.grid(padx=5, pady=5)
        self.tree_button = tk.Button(
            self.frame, text="Show Tree", command=self.make_tree)
        self.take_button = tk.Button(
            self.frame, text="Take Stones", command=self.take_stones)
        self.shuffle_button = tk.Button(
            self.frame, text="Reset Game", command=self.reset_game)
        self.change_game_button = tk.Button(
            self.frame, text="Change Game", command=self.change_game)
        # self.computer_start_button = tk.Button(
        #     self.frame, text="Computer Start", command=self.computer_turn)

        self.original_stones = self.minimax.game.state.copy()
        self.state = []
        self.player_stones = []
        self.computer_stones = []
        self.computer_score = 0
        self.player_score = 0
        self.init_labels()
        self.set_styling()
        self.update_status()

    def init_labels(self):
        """
        Initialize the labels
        """
        self.label = tk.Label(
            self.frame, text=self.minimax.game.rules, fg='black')
        self.status_label = tk.Label(
            self.root, text="")
        self.score_label = tk.Label(
            self.root, text="")

        self.shuffle_button.grid(row=1, column=0)
        self.take_button.grid(row=1, column=1)
        self.tree_button.grid(row=1, column=2)
        self.status_label.grid(row=3, column=0)
        self.score_label.grid(row=4, column=0)
        self.canvas.grid(row=5, column=0)
        self.change_game_button.grid(row=2, column=1)
        # self.computer_start_button.grid(row=2, column=2)

    def change_game(self):
        """
        Change the game
        """
        if isinstance(self.minimax.game, StoneGame):
            self.minimax = Minimax(TicTacToe())
            self.root.destroy()
            root = tk.Tk()
            game = TicTacToeGUI(root, self.minimax)
            root.mainloop()
        else:
            self.minimax = Minimax(StoneGame())
            self.root.destroy()
            root = tk.Tk()
            game = StoneGameGUI(root, self.minimax)
            root.mainloop()

    def set_styling(self):
        """
        Set the styling for the buttons
        """
        button_list = [self.tree_button, self.take_button, self.shuffle_button]
        for button in button_list:
            button.config(font=("Comic Sans MS", 14))
            button.config(bg='light green')
            button.config(fg='black')
            button.config(relief='raised')
            button.config(borderwidth=2)
            button.config(cursor='hand2')

    def make_tree(self):
        """
        Make the tree
        """
        self.minimax.game_tree.plot_mini_max_tree(label_type="state")

    def reset_game(self):
        self.minimax.game.reset()
        self.minimax.game.state = self.original_stones.copy()
        self.update_status()

    def pile_click(self, event, index):
        self.take_stone(index)

    def take_stone(self, i):
        if i > 2 or i < 0:
            messagebox.showerror("Error", "Please select a valid pile.")
        else:
            self.take_stones(i + 1)

    def update_status(self):
        status = f"Remaining Stones: {self.minimax.game.state}"
        self.status_label.config(text=status)
        self.score_label.config(
            text=f"Player: {self.player_score} Computer: {self.computer_score}")
        self.canvas.delete("all")
        self.piles = []
        for i in range(len(self.minimax.game.state)):
            self.piles.append(
                self.canvas.create_rectangle(50 * i, 0, 50 * (i + 1), 50,
                                             fill='orange',
                                             outline='black', width=2, activefill='light grey' if i < 3 else 'red',
                                             activeoutline='black'))
            self.canvas.tag_bind(self.piles[i], '<Button-1>',
                                 lambda event, index=i: self.pile_click(event, index), add='+')
            self.canvas.create_text(
                50 * i + 25, 25, text=str(self.minimax.game.state[i]), font=("Arial", 14))

        for i in range(len(self.player_stones)):
            self.canvas.create_rectangle(
                50 * i, 50, 50 * (i + 1), 100, fill='grey')
            self.canvas.create_text(
                50 * i + 25, 75, text=str(self.player_stones[i]),
                font=("Arial", 14))

        # add stones taken by the computer in red
        for i in range(len(self.computer_stones)):
            self.canvas.create_rectangle(
                50 * i, 100, 50 * (i + 1), 150, fill='red')
            self.canvas.create_text(
                50 * i + 25, 125, text=str(self.computer_stones[i]),
                font=("Arial", 14))

        if len(self.minimax.game.state) == 0:
            self.results()

    def take_stones(self, stone_index=None):
        """
        Take stones from the pile
        """
        num_stones = 0
        if stone_index is not None:
            num_stones = stone_index
        else:
            raise ValueError("Please select a valid pile.")
        for i in range(num_stones):
            stone = self.minimax.game.state[i]
            self.player_stones.append(stone)
        for i in range(num_stones):
            self.player_score += self.minimax.game.state[i]
        newState, _ = self.minimax.result(
            self.minimax.game.state, num_stones)
        self.minimax.game.state = newState
        self.update_status()
        self.computer_turn()

    def computer_turn(self):
        """
        Computer's turn
        """
        _, action = self.minimax.ply(self.minimax.game.state.copy())
        for i in range(action):
            self.computer_score += self.minimax.game.state[i]
            self.computer_stones.append(self.minimax.game.state[i])
        newState, _ = self.minimax.result(
            self.minimax.game.state, action)
        self.minimax.game.state = newState
        self.update_status()

    def results(self):
        """
        Display the results of the game
        """
        # move the stones to the last player
        if self.player_score > self.computer_score:
            messagebox.showinfo("Results", "You win with a score of " +
                                str(self.player_score) + " to " + str(self.computer_score) + "!")
        elif self.player_score < self.computer_score:
            messagebox.showinfo("Results", "You lose! The computer scored " +
                                str(self.computer_score) + " to your " + str(self.player_score) + ".")
        else:
            messagebox.showinfo("Results", "It's a tie!")
        # ask to play again
        play_again = messagebox.askyesno(
            "Play Again", "Do you want to play again?")
        if play_again:
            self.reset_game()
        else:
            self.root.destroy()


class TicTacToeGUI(GameGUI):
    """
    TicTacToeGUI class
    """

    def __init__(self, root, minimax):
        super().__init__(root, minimax)
        self.root.title("Tic Tac Toe")
        self.canvas.bind("<Button-1>", self.click)
        self.computer_player = -1

    def click(self, event):
        """
        Handle the mouse click event
        """
        x, y = event.x, event.y
        row, col = x // 100, y // 100
        if self.minimax.game.state[row * 3 + col] != 0:
            return

        self.minimax.game.state[row * 3 + col] = - self.computer_player
        print(f'Player takes action {row * 3 + col}')
        print(self.minimax.game.state)
        self.update_status()
        self.computer_turn()

    def update_status(self):
        """
        Update tic tac toe status with X and O
        """
        self.canvas.delete("all")
        for i in range(3):
            for j in range(3):
                x1, y1 = i * 100, j * 100
                x2, y2 = (i + 1) * 100, (j + 1) * 100
                if self.minimax.game.state[i * 3 + j] == -1:
                    self.canvas.create_oval(
                        x1, y1, x2, y2, outline="black", width=2)
                elif self.minimax.game.state[i * 3 + j] == 1:
                    self.canvas.create_line(
                        x1, y1, x2, y2, fill="black", width=2)
                    self.canvas.create_line(
                        x2, y1, x1, y2, fill="black", width=2)
        # add grid lines
        self.canvas.create_line(100, 0, 100, 300, fill="black", width=2)
        self.canvas.create_line(200, 0, 200, 300, fill="black", width=2)
        self.canvas.create_line(0, 100, 300, 100, fill="black", width=2)
        self.canvas.create_line(0, 200, 300, 200, fill="black", width=2)

        print(f'current state: {self.minimax.game.state}')
        print(f'check winner: {self.minimax.game.is_terminal()}')
        if self.minimax.game.is_terminal(self.minimax.game.state):
            self.results()

    def computer_turn(self):
        """
        Computer's turn
        """
        if sum(self.minimax.game.state) == 0:
            self.computer_player = 1
        elif sum(self.minimax.game.state) == 1:
            self.computer_player = -1
        _, action = self.minimax.get_ply_successors(
            self.minimax.game.state.copy())
        print(f'Computer takes action {action}')
        if action is None:
            # computer won!
            print("Computer won!")
        self.minimax.game.state[action] = self.computer_player
        self.update_status()

    def results(self):
        """
        Display the results of the game based on the utility
        """
        utility = self.minimax.game.utility(self.minimax.game.state, 1)
        if utility == 1:
            messagebox.showinfo("Results", "You win!")
        elif utility == -1:
            messagebox.showinfo("Results", "You lose!")
        else:
            messagebox.showinfo("Results", "It's a tie!")
        # ask to play again
        play_again = messagebox.askyesno(
            "Play Again", "Do you want to play again?")
        if play_again:
            self.reset_game()
            self.root.mainloop()
        else:
            self.root.destroy()


class StoneGameGUI(GameGUI):
    """
    StoneGameGUI class
    """

    def __init__(self, root, minimax):
        super().__init__(root, minimax)
        self.root.title("Stone Game")
        self.canvas.bind("<Button-1>", self.click)

    def click(self, event):
        """
        Handle the mouse click event
        """
        x, y = event.x, event.y
        pile = x // 50
        self.take_stone(pile)

    def reset_game(self):
        self.player_stones = []
        self.piles = []
        self.player_score = 0
        self.computer_score = 0
        self.minimax.reset()
        return super().reset_game()
