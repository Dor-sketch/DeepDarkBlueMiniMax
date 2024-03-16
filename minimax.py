"""
This is a simple game of taking stones.
It is played between the player and the computer,
where the player and the computer take turns taking stones from a pile.
The player can take 1-3 stones from the pile and the computer uses
the minimax algorithm to determine the best move to make.
The game ends when there are no more stones in the pile and the player with the most stones wins.
The game is implemented using tkinter for the GUI and networkx for the minimax tree visualization.
"""
from math import inf
from typing import List
from game_tic_tac_toe import TicTacToe
from game_tree import GameTree

MAX = 1
MIN = -1

class Minimax:
    """
    Minimax class
    """

    def __init__(self, GameLogic):
        """
        Initializes the Minimax class
        """
        self.game = GameLogic



    def play(self, state: List[int], iterations: int = 4, player="max"):
        """
        Determines the winner of the game
        """
        self.state = state
        self.game_tree = GameTree(state)
        dif, _ = self.max_value(state, -float('inf'),
                                float('inf'), depth=0, iterations=iterations)
        if dif > 0:
            return "Max"
        elif dif < 0:
            return "Min"
        else:
            return "Tie"

    def minimax_move(self, state: List[int], player: str = None, depth:int = 0, iterations: int = 10) -> (int, int):
        """
        Returns the best move for the computer
        """
        cur_depth = 0
        for cell in state:
            if cell != 0:
                cur_depth += 1
        if cur_depth % 2 == 0:
            # max player
            _, move = self.max_value(state, -float('inf'), float('inf'), depth, iterations)
        else:
            # min player
            _, move = self.min_value(state, -float('inf'), float('inf'), depth, iterations)
        return move

    def max_value(self, state: List[int], alpha: int, beta: int, depth: int, iterations: int = 10) -> (int, int):
        """
        Returns the maximum value and the action that leads to that value
        """
        if self.game.is_terminal(state):
            utility = self.game.utility(state)
            return utility, None

        best_move = None
        v = -inf # initial value of max node
        for a in self.game.actions(state):
            # TODO: implemet killer move heuristic
            new_state = self.game.result(state, a)
            v2, _ = self.min_value(
                new_state, alpha, beta, depth + 1, iterations - 1)
            if v <= v2:
                v = v2
                best_move = a
            # alpha = max(alpha, v2)
            # if beta <= v:
            #     break
        # updating best move and value wile backtracking
        return v, best_move

    def min_value(self, state: List[int], alpha: int, beta: int, depth: int, iterations: int = 10) -> (int, int):
        """
        Returns the minimum value and the action that leads to that value
        """
        v = inf
        best_move = None
        if self.game.is_terminal(state, MIN):
            v = self.game.utility(state, MIN)
        else:
            for a in self.game.actions(state):
                new_state = self.game.result(state, a)
                # Adjusted key to include newState and updated dif
                v2, a2 = self.max_value(
                    new_state, alpha, beta, depth + 1, iterations-1)
                if v2 < v:
                    best_move = a
                    v = v2
                # beta = min(beta, v2)
                # if v <= alpha:
                #     break
        return v, best_move


if __name__ == "__main__":
    # test why tic tac toe is not working
    game = TicTacToe()
    minimax = Minimax(game)
    # minimax.play([0, 0, 0, 0, 0, 0, 0, 0, 0], 4)
    # # minimax.game_tree.plot_mini_max_tree()
    # nodoe_id = minimax.game_tree.generate_id([0, 0, 1, 0, 0, 0, 0, 0, 0], 1, -1)
    # minimax.game_tree.print_game_tree_from_node(nodoe_id)
    state = [0, 0, 1, 0, 0, 0, 0, 0, 0]
    print(game.print_state(state))
    print('-------------------')

    v, a = minimax.min_value(state, -float('inf'), float('inf'), 0, 4)
    print(v, a)
    state = game.result(state, a)
    print(game.print_state(state))
    print('-------------------')

    state = game.result(state, 0)
    print(game.print_state(state))
    print('-------------------')

    v, a = minimax.max_value(state, -float('inf'), float('inf'), 0, 4)
    print(v, a)
    state = game.result(state, a)
    print(game.print_state(state))
    print('-------------------')

    state = game.result(state, 8)
    print(game.print_state(state))
    print('-------------------')

    v, a = minimax.max_value(state, -float('inf'), float('inf'), 0, 4)
    print(v, a)
    state = game.result(state, a)
    print(game.print_state(state))
    print('-------------------')


    state = game.result(state, 1)
    print(game.print_state(state))
    print('-------------------')
