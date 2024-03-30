import pygame
from minimax import Minimax
from game_tic_tac_toe import TicTacToe
import pygame.gfxdraw
import numpy as np
import pygame.gfxdraw


class GameGUI:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((600, 600))
        self.clock = pygame.time.Clock()
        self.game = TicTacToe()
        self.minimax = Minimax(self.game)
        self.board = self.game.state
        self.player_turn = True
        pygame.display.set_caption("Deep Dark Blue Mini Max Pro")

    def draw_board(self):
        # Create a surface with a vertical gradient
        gradient = pygame.Surface((600, 600))
        for i in range(600):
            color = np.array([0, 0, 0]) + i * np.array([255, 255, 255]) / 800
            pygame.draw.line(gradient, color, (0, i), (600, i))

        # Blit the gradient onto the screen
        self.screen.blit(gradient, (0, 0))
        # Create a surface for the glowing effect
        glow = pygame.Surface((600, 600), pygame.SRCALPHA)
        # iphone pro max shade
        glow.fill((160, 160, 152, 100))  # Changed color to blue
        self.screen.blit(glow, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # Draw lines around the block to create a 3D shadow effect
        for i in range(1, 5):
            color = np.array([0, 0, 0]) + i * np.array([255, 255, 255]) / 5
            pygame.draw.line(self.screen, color, (200 * i, 0), (200 * i, 600), 5)
            pygame.draw.line(self.screen, color, (0, 200 * i), (600, 200 * i), 5)

        # Create a surface for the lighting effect
        lighting = pygame.Surface((600, 600), pygame.SRCALPHA)
        lighting.fill((255, 255, 255, 100))  # Reduced intensity
        self.screen.blit(lighting, (0, 0),
                         special_flags=pygame.BLEND_RGBA_MULT)



        # Draw the X's and O's with a 3D effect
        # Draw the X's and O's with a 3D effect
        for y in range(3):
            for x in range(3):
                center = (200 * x + 100, 200 * y + 100)
                if self.board[y * 3 + x] == 1:  # Draw X
                    for i in range(10):  # Increase range for thicker X
                        pygame.draw.aaline(self.screen, (255 - i * 15, i * 5, 0), (center[0] - 60 + i, center[1] - 60 + i), (
                            center[0] + 60 + i, center[1] + 60 + i), 3)  # Increase width for thicker line
                        pygame.draw.aaline(self.screen, (255 - i * 15, i * 5, 0), (center[0] + 60 + i, center[1] - 60 + i), (
                            center[0] - 60 + i, center[1] + 60 + i), 3)  # Increase width for thicker line

                elif self.board[y * 3 + x] == -1:  # Draw O
                    for i in range(10):  # Increase range for thicker O
                        # Increase width for thicker circle
                        pygame.gfxdraw.aacircle(
                            self.screen, center[0], center[1], 50 + i, (11, 11, 255 - i * 15))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN and self.player_turn:
                x, y = pygame.mouse.get_pos()
                # Corrected action calculation for board indexing
                column = x // 200
                row = y // 200
                if 0 <= column <= 2 and 0 <= row <= 2:  # Check if the click is within bounds
                    action = row * 3 + column
                    if action in self.game.actions(self.board):
                        self.board = self.game.result(self.board, action)
                        self.player_turn = False
        return True

    def display_message(self, message):
        pygame.font.init()
        myfont = pygame.font.SysFont('Comic Sans MS', 30)
        textsurface = myfont.render(message, False, (255, 255, 255))
        self.screen.blit(textsurface, (200, 550))

    def play_again(self):
        self.display_message("Play Again?")
        pygame.display.flip()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    x, y = pygame.mouse.get_pos()
                    if 200 <= x <= 400 and 550 <= y <= 580:  # Check if the click is within the "Play Again?" message
                        self.game = TicTacToe()
                        self.board = self.game.state
                        self.player_turn = True
                        return True
            self.clock.tick(60)

    def run(self):
        running = True
        while running:
            self.draw_board()
            pygame.display.flip()
            running = self.handle_events()
            self.clock.tick(60)
            if not self.player_turn and not self.game.is_terminal(self.board):
                action = self.minimax.minimax_move(
                    self.board.copy())  # Use the current board state
                self.board = self.game.result(self.board, action)
                self.draw_board()

                self.player_turn = True
            if self.game.is_terminal(self.board):
                running = self.play_again()


if __name__ == "__main__":
    gui = GameGUI()

    gui.run()
