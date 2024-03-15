

class MainMenu:
    def __init__(self, master):
        self.master = master
        self.master.title("Game Selector")
        self.frame = tk.Frame(self.master)
        self.tic_tac_toe_button = tk.Button(
            self.frame, text="Tic Tac Toe", command=self.open_tic_tac_toe)
        self.tic_tac_toe_button.pack()
        self.stone_game_button = tk.Button(
            self.frame, text="Stone Game", command=self.open_stone_game)
        self.stone_game_button.pack()
        self.frame.pack()

    def open_tic_tac_toe(self):
        self.new_window = tk.Toplevel(self.master)
        self.app = TicTacToe(self.new_window)

    def open_stone_game(self):
        # Placeholder for Stone Game logic
        self.new_window = tk.Toplevel(self.master)
        tk.Label(self.new_window, text="Stone Game Placeholder").pack()
