"""
This is a simple game of taking stones.
It is played between the player and the computer,
where the player and the computer take turns taking stones from a pile.
The player can take 1-3 stones from the pile and the computer uses
the minimax algorithm to determine the best move to make.
The game ends when there are no more stones in the pile and the player with the most stones wins.
The game is implemented using tkinter for the GUI and networkx for the minimax tree visualization.
"""
import random
from math import inf
from typing import List
from tkinter import messagebox
import tkinter as tk
import networkx as nx
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt


class Minimax:
    """
    Minimax class
    """
    def __init__(self):
        self.G = nx.DiGraph()
        self.stoneValue = []

    def stoneGameIII(self, stoneValue):
        """
        Determines the winner of the game
        """
        self.stoneValue = stoneValue
        dif, _ = self.max_value(stoneValue, -float('inf'),
                                float('inf'), 0, tree_level=0)
        if dif > 0:
            return "Max"
        elif dif < 0:
            return "Min"
        else:
            return "Tie"

    def ply(self, state: List[int], max_depth: int = 20, player="max"):
        """
        Returns the computer's move based on the current state
        return computer optimal move
        crop state to max_depth
        """
        state = state[:max_depth]
        v, a = self.max_value(state, -inf, inf, 0, tree_level=0)
        return v, a

    def actions(self, state: List[int]) -> List[int]:
        """
        Generates a list of possible actions based on the current state
        """
        return [i for i in range(1, min(3, len(state)) + 1)]

    def result(self, state: List[int], action: int) -> (List[int], int):
        """
        Returns the resulting state and the score gained by taking 'action' number of stones
        """
        score = sum(state[:action])
        return state[action:], score

    def max_value(self, state: List[int], alpha: int, beta: int, dif: int, tree_level: int) -> (int, int):
        if len(state) == 0:
            self.G.nodes[str(tree_level) + str(tuple(state)) +
                         str(dif)]['value'] = dif
            return dif, 0
        node_id = str(tree_level) + str(tuple(state)) + str(dif)
        if node_id not in self.G:
            self.G.add_node(node_id)
            self.G.nodes[node_id]['level'] = tree_level

        move = 0
        v = -inf
        for a in self.actions(state):
            newState, score = self.result(state, a)
            # Adjusted key to include newState and updated dif
            son_id = str(tree_level + 1) + \
                str(tuple(newState)) + str(dif + score)
            self.G.add_node(son_id)
            self.G.nodes[son_id]['level'] = tree_level + 1
            self.G.add_edge(node_id, son_id)
            v2, a2 = self.min_value(
                newState, alpha, beta, dif + score, tree_level + 1)
            if v < v2:
                v = v2
                if a2 != 0:
                    move = a2
                else:
                    move = a
            alpha = max(alpha, v2)
            if beta <= v:
                self.G.nodes[son_id]['value'] = inf
                break
        self.G.nodes[node_id]['value'] = v
        return v, move

    def min_value(self, state: List[int], alpha: int, beta: int, dif: int, tree_level: int) -> (int, int):
        if len(state) == 0:
            self.G.nodes[str(tree_level) + str(tuple(state)) +
                         str(dif)]['value'] = dif
            return dif, 0
        node_id = str(tree_level) + str(tuple(state)) + str(dif)
        if node_id not in self.G:
            self.G.add_node(node_id)
            self.G.nodes[node_id]['level'] = tree_level

        v = inf
        move = 0
        for a in self.actions(state):
            newState, score = self.result(state, a)
            # Adjusted key to include newState and updated dif
            # In your min_value method
            son_id = str(tree_level + 1) + \
                str(tuple(newState)) + str(dif - score)
            self.G.add_node(son_id)
            self.G.nodes[son_id]['level'] = tree_level + 1

            self.G.add_edge(node_id, son_id)
            v2, a2 = self.max_value(
                newState, alpha, beta, dif - score, tree_level + 1)
            if v > v2:
                if a2 != 0:
                    move = a2
                else:
                    move = a
                v = v2
            beta = min(beta, v2)
            if v <= alpha:
                self.G.nodes[son_id]['value'] = -inf
                print(f'Pruning {son_id} with value {v2}')
                break
        # update node_id to be the return value
        self.G.nodes[node_id]['value'] = v
        return v, move

    def plot_mini_max_tree(self):
        """
        Plots the minimax tree
        """
        G = self.G

        # Get nodes at odd and even levels
        odd_level_nodes = [node for node, data in G.nodes(
            data=True) if data['level'] % 2 == 0]
        even_level_nodes = [node for node, data in G.nodes(
            data=True) if data['level'] % 2 == 1]

        # Use graphviz_layout with dot for a tree-like layout
        pos = graphviz_layout(G, prog='dot')

        # Draw nodes at odd levels with triangle shape
        nx.draw_networkx_nodes(
            G, pos, nodelist=odd_level_nodes, node_shape='^', node_color='lightblue')

        # Draw nodes at even levels with upside-down triangle shape
        nx.draw_networkx_nodes(
            G, pos, nodelist=even_level_nodes, node_shape='v', node_color='red')

        # Draw edges and labels for all nodes
        nx.draw_networkx_edges(G, pos, arrowsize=20)
        nx.draw_networkx_labels(
            G, pos, labels={node: data['value'] for node, data in G.nodes(data=True)})

        plt.show()


class StoneGameGUI:
    """
    StoneGameGUI class
    """
    def __init__(self, root, game_logic):
        self.root = root
        self.player_score = 0
        self.computer_score = 0
        self.game_logic = game_logic
        self.root.title("My Stone Game")
        self.canvas = tk.Canvas(self.root, width=1200,
                                height=100, bg='light blue')
        self.frame = tk.Frame(self.root)
        self.frame.grid(padx=5, pady=5)

        self.entry = tk.Entry(self.frame)
        self.tree_button = tk.Button(
            self.frame, text="Show Tree", command=self.make_tree)

        self.take_button = tk.Button(
            self.frame, text="Take Stones", command=self.take_stones)

        self.shuffle_button = tk.Button(
            self.frame, text="Shuffle Stones", command=self.shuffle_stones)

        self.init_labels()

        self.original_stones = self.game_logic.stoneValue.copy()
        self.piles = []
        self.player_stones = []
        self.set_styling()
        self.update_status()

    def init_labels(self):
        """
        Initialize the labels
        """
        self.label = tk.Label(
            self.frame, text="Select number of stones to take (1-3):", fg='black')
        self.status_label = tk.Label(
            self.root, text="")
        self.score_label = tk.Label(
            self.root, text="")
        self.label.grid(row=0, column=0)
        self.entry.grid(row=0, column=1)
        self.shuffle_button.grid(row=1, column=0)
        self.take_button.grid(row=1, column=1)
        self.tree_button.grid(row=1, column=2)
        self.status_label.grid(row=3, column=0)
        self.score_label.grid(row=4, column=0)
        self.canvas.grid(row=5, column=0)


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
        game = Minimax()
        game.stoneValue = self.game_logic.stoneValue.copy()
        if len(game.stoneValue) > 20:
            game.stoneValue = game.stoneValue[:20]
        game.stoneGameIII(game.stoneValue)
        game.plot_mini_max_tree()

    def shuffle_stones(self):
        self.reset_game()
        new_stone_values = [random.randint(0, 20)
                            for _ in range(random.randint(21, 25))]
        self.original_stones = new_stone_values
        self.game_logic.stoneValue = new_stone_values
        self.update_status()

    def pile_click(self, event, index):
        self.take_stone(index)

    def take_stone(self, i):
        if i > 2 or i < 0:
            messagebox.showerror("Error", "Please select a valid pile.")
        else:
            self.take_stones(i + 1)

    def update_status(self):
        status = f"Remaining Stones: {self.game_logic.stoneValue}"
        self.status_label.config(text=status)
        self.score_label.config(
            text=f"Player: {self.player_score} Computer: {self.computer_score}")
        self.canvas.delete("all")
        self.piles = []
        for i in range(len(self.game_logic.stoneValue)):
            self.piles.append(
                self.canvas.create_rectangle(50 * i, 0, 50 * (i + 1), 50,
                                             fill='orange',
                                             outline='black', width=2, activefill='light grey' if i < 3 else 'red',
                                             activeoutline='black'))
            self.canvas.tag_bind(self.piles[i], '<Button-1>',
                                 lambda event, index=i: self.pile_click(event, index), add='+')
            self.canvas.create_text(
                50 * i + 25, 25, text=str(self.game_logic.stoneValue[i]), font=("Arial", 14))

        for i in range(len(self.player_stones)):
            self.canvas.create_rectangle(
                50 * i, 50, 50 * (i + 1), 100, fill='grey')
            self.canvas.create_text(
                50 * i + 25, 75, text=str(self.player_stones[i]),
                font=("Arial", 14))

        if len(self.game_logic.stoneValue) == 0:
            self.results()

    def take_stones(self, stone_index=None):
        """
        Take stones from the pile
        """
        num_stones = 0
        if stone_index is not None:
            num_stones = stone_index
        else:
            try:
                num_stones = int(self.entry.get())
                if num_stones < 1 or num_stones > 3:
                    raise ValueError("Please enter a number between 1 and 3.")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
            except Exception as e:
                messagebox.showerror("Error", str(e))
        for i in range(num_stones):
            stone = self.game_logic.stoneValue[i]
            self.player_stones.append(stone)
        for i in range(num_stones):
            self.player_score += self.game_logic.stoneValue[i]
        newState, _ = self.game_logic.result(
            self.game_logic.stoneValue, num_stones)
        self.game_logic.stoneValue = newState
        self.update_status()
        self.computer_turn()

    def computer_turn(self):
        """
        Computer's turn
        """
        _, action = self.game_logic.ply(self.game_logic.stoneValue.copy())
        for i in range(action):
            self.computer_score += self.game_logic.stoneValue[i]
        newState, _ = self.game_logic.result(
            self.game_logic.stoneValue, action)
        self.game_logic.stoneValue = newState
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
            self.shuffle_stones()
        else:
            self.root.destroy()

    def reset_game(self):
        """
        Reset the game
        """
        self.player_score = 0
        self.computer_score = 0
        self.piles = []
        self.player_stones = []


def main():
    """
    Run the StoneGameGUI
    """
    root = tk.Tk()
    game_logic = Minimax()
    initial_stone_values = [random.randint(-10, 10)
                            for _ in range(random.randint(14,17))]
    game_logic.stoneValue = initial_stone_values
    game = StoneGameGUI(root, game_logic)
    game.shuffle_stones()
    root.mainloop()


if __name__ == "__main__":
    main()
