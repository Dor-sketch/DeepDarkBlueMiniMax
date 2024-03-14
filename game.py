"""
This file contains the classes for the game logic of the games StoneGame and TicTacToe
"""

from typing import List
import random


class GameLogic:
    """
    GameLogic class
    """

    def __init__(self):
        self.state = []
        self.rules = ""
        self.player_score = 0
        self.computer_score = 0

    def actions(self, state: List[int]) -> List[int]:
        """
        Generates a list of possible actions based on the current state
        """
        pass

    def result(self, state: List[int], action: int) -> (List[int], int):
        """
        Returns the resulting state and the score gained by taking 'action' number of stones
        """
        pass

    def reset(self):
        self.state = []
        self.player_score = 0
        self.computer_score = 0

    def check_winner(self, state: List[int]) -> str:
        """
        Determines the winner of the game
        """
        pass


class StoneGame(GameLogic):
    """
    StoneGame class
    """

    def __init__(self):
        super().__init__()
        self.rules = "The game starts with a pile of stones. Players take turns taking 1, 2, or 3 stones from the pile. The player who takes the last stone loses."
        self.state = [random.randint(0, 10)
                      for _ in range(random.randint(14, 17))]

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

    def utility(self, state: List[int], player: int) -> int:
        """
        Determines the utility of the current state
        """
        # if len(state) == 0:
        #     if player == 1:
        #         self.player_score += 1
        #     else:
        #         self.computer_score += 1
        return 0

    def reset(self):
        """
        Resets the game state
        """
        super().reset()
        self.state = [i for i in range(15)]

    def check_winner(self, state: List[int]) -> str:
        """
        Determines the winner of the game
        """
        if len(state) == 0:
            if self.player_score > self.computer_score:
                return "Player"
            elif self.player_score < self.computer_score:
                return "Computer"
            else:
                return "Tie"
        return "No winner yet"

    def __type__(self):
        return "StoneGame"


class TicTacToe(GameLogic):
    """
    TicTacToe class
    """

    def __init__(self):
        super().__init__()
        self.rules = "The game is played on a 3x3 grid. Players take turns placing their symbol (X or O) in an empty square. The player who gets 3 of their symbols in a row wins."
        self.state = [0 for _ in range(9)]

    def actions(self, state: List[int]) -> List[int]:
        """
        Generates a list of possible actions based on the current state
        """
        return [i for i in range(len(state)) if state[i] == 0]

    def utility(self, state: List[int], player: int) -> int:
        """
        Determines the utility of the current state
        """
        if self.check_winner(state) == "Player":
            return 1
        elif self.check_winner(state) == "Computer":
            return -1
        return 0

    def result(self, state: List[int], action: int) -> (List[int], int):
        """
        Returns the resulting state and the score gained by taking 'action'
        """
        newState = state.copy()
        # check if last move was by player using number of 1's and -1's
        if sum(state) > 0:
            newState[action] = -1
        else:
            newState[action] = 1
        return newState, 0

    def reset(self):
        """
        Resets the game state
        """
        super().reset()
        self.state = [0 for _ in range(9)]

    def check_winner(self, state: List[int] = None) -> str:
        """
        Determines the winner of the game
        """
        if state is None:
            state = self.state
        print(state)
        if state[0] == state[1] == state[2] == 1 or state[3] == state[4] == state[5] == 1 or state[6] == state[7] == state[8] == 1 or state[0] == state[3] == state[6] == 1 or state[1] == state[4] == state[7] == 1 or state[2] == state[5] == state[8] == 1 or state[0] == state[4] == state[8] == 1 or state[2] == state[4] == state[6] == 1:
            return "Player"
        elif state[0] == state[1] == state[2] == -1 or state[3] == state[4] == state[5] == -1 or state[6] == state[7] == state[8] == -1 or state[0] == state[3] == state[6] == -1 or state[1] == state[4] == state[7] == -1 or state[2] == state[5] == state[8] == -1 or state[0] == state[4] == state[8] == -1 or state[2] == state[4] == state[6] == -1:
            return "Computer"
        elif 0 not in state:
            return "Tie"
        return "No winner yet"

    def __type__(self):
        return "TicTacToe"
