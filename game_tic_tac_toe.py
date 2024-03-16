"""
TicTacToe class
"""

from typing import List
from game import GameLogic

GOAL_STATES = [  # 8 possible winning combinations
    [0, 1, 2],  # top row
    [3, 4, 5],  # middle row
    [6, 7, 8],  # bottom row
    [0, 3, 6],  # left column
    [1, 4, 7],  # middle column
    [2, 5, 8],  # right column
    [0, 4, 8],  # diagonal
    [2, 4, 6]  # diagonal
]

MAX_PLAYER = 'X'
MIN_PLAYER = 'O'


class TicTacToe(GameLogic):
    """
    TicTacToe class
    """

    def __init__(self):
        super().__init__()
        self.rules = "The game is played on a 3x3 grid. Players take turns placing their symbol (X or O) in an empty square. The player who gets 3 of their symbols in a row wins."
        self.state = [0 for _ in range(9)]  # initialize empty board, s_0

    def actions(self, state: List[int]) -> List[int]:
        """
        Generates a list of possible actions based on the current state
        """
        # if there is already a winner, return empty list
        if self.is_terminal(state):
            return []
        return [i for i in range(len(state)) if state[i] == 0]

    def utility(self, state: List[int], player: int) -> int:
        """
        Determines the utility of the current state
        """
        for player in [-1, 1]:
            for combo in GOAL_STATES:
                if all(state[i] == player for i in combo):
                    return player
        return 0

    def result(self, state: List[int], action: int) -> (List[int], int):
        """
        Returns the resulting state given the action on the current state

        Args:
            state (List[int]): current state
            action (int): action to be taken
        """
        new_state = state.copy()
        # check if last move was by player using number of 1's and -1's
        if sum(state) > 0:
            # last move was by the player (X) because there are more 1's
            new_state[action] = -1
        else:
            new_state[action] = 1
        return new_state

    def reset(self):
        """
        Resets the game state
        """
        super().reset()
        self.state = [0 for _ in range(9)]

    def is_terminal(self, state: List[int] = None, player: int = 1) -> bool:
        """
        Determines if the game is in a terminal state
        """
        if state is None:
            state = self.state
        # check if the board is full (no more possible moves)
        if 0 not in state:
            return True
        # check if there is a winner
        for player in [1, -1]:
            for combo in GOAL_STATES:
                if all(state[i] == player for i in combo):
                    return True
        return False

    def __type__(self):
        return "TicTacToe"

    def print_state(self, state: List[int] = None) -> str:
        """
        return pretty print of the game state
        """
        if state is None:
            state = self.state
        symbols = {0: ' ', 1: 'X', -1: 'O'}
        ret = ""
        for i, s in enumerate(state):
            ret += symbols[s]
            if i % 3 == 2:
                ret += "\n"
            else:
                ret += " | "
        return ret

    def __str__(self):
        """
        return pretty print of the game state
        """
        return self.print_state(self.state)
