import tkinter as tk
from tkinter import messagebox
import random

class TicTacToe:
    def __init__(self):
        self.board = [' ' for _ in range(9)]
        self.current_winner = None

    def print_board(self):
        for row in [self.board[i*3:(i+1)*3] for i in range(3)]:
            print('| ' + ' | '.join(row) + ' |')

    @staticmethod
    def print_board_nums():
        number_board = [[str(i) for i in range(j*3, (j+1)*3)] for j in range(3)]
        for row in number_board:
            print('| ' + ' | '.join(row) + ' |')

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def empty_squares(self):
        return ' ' in self.board

    def num_empty_squares(self):
        return self.board.count(' ')

    def make_move(self, square, letter):
        if self.board[square] == ' ':
            self.board[square] = letter
            if self.winner(square, letter):
                self.current_winner = letter
            return True
        return False

    def winner(self, square, letter):
        row_ind = square // 3
        row = self.board[row_ind*3:(row_ind+1)*3]
        if all([spot == letter for spot in row]):
            return True
        col_ind = square % 3
        column = [self.board[col_ind+i*3] for i in range(3)]
        if all([spot == letter for spot in column]):
            return True
        if square % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            if all([spot == letter for spot in diagonal1]):
                return True
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal2]):
                return True
        return False


def play(game, x_player, o_player, print_game=True):
    letter = 'X'
    while game.empty_squares():
        if letter == 'O':
            square = o_player.get_move(game)
        else:
            square = x_player.get_move(game)

        if game.make_move(square, letter):
            if game.current_winner:
                return letter

            letter = 'O' if letter == 'X' else 'X'

    return 'Tie'

class HumanPlayer:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        return None

class AIPlayer:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = 4
        else:
            square = self.minimax(game, self.letter)['position']
        return square

    def minimax(self, state, player):
        max_player = self.letter
        other_player = 'O' if player == 'X' else 'X'

        if state.current_winner == other_player:
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                        state.num_empty_squares() + 1)}
        elif not state.empty_squares():
            return {'position': None, 'score': 0}

        if player == max_player:
            best = {'position': None, 'score': -float('inf')}
        else:
            best = {'position': None, 'score': float('inf')}

        for possible_move in state.available_moves():
            state.make_move(possible_move, player)
            sim_score = self.minimax(state, other_player)

            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move

            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score
        return best

class RandomAIPlayer:
    def __init__(self, letter):
        self.letter = letter

    def get_move(self, game):
        return random.choice(game.available_moves())

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        window_width = 300
        window_height = 300
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2

        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.tic_tac_toe = TicTacToe()
        self.current_player = 'X'
        self.game_buttons = []

        for i in range(3):
            for j in range(3):
                button = tk.Button(self.root, text='', font=('Arial', 20), width=5, height=2,
                                   command=lambda i=i, j=j: self.on_button_click(i, j))
                button.grid(row=i, column=j)
                self.game_buttons.append(button)

    def on_button_click(self, i, j):
        if self.tic_tac_toe.board[i * 3 + j] == ' ':
            self.tic_tac_toe.make_move(i * 3 + j, self.current_player)
            self.update_board()
            winner = self.tic_tac_toe.current_winner
            if winner:
                messagebox.showinfo("Game Over", f"{winner} wins!")
                self.root.quit()
            elif not self.tic_tac_toe.empty_squares():
                messagebox.showinfo("Game Over", "It's a tie!")
                self.root.quit()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                if self.current_player == 'O':
                    self.ai_move()

    def update_board(self):
        for i in range(3):
            for j in range(3):
                self.game_buttons[i * 3 + j].config(text=self.tic_tac_toe.board[i * 3 + j], bg='white')
                if self.tic_tac_toe.board[i * 3 + j] == 'X':
                    self.game_buttons[i * 3 + j].config(bg='skyblue')
                elif self.tic_tac_toe.board[i * 3 + j] == 'O':
                    self.game_buttons[i * 3 + j].config(bg='lightcoral')

    def ai_move(self):
        square = RandomAIPlayer('O').get_move(self.tic_tac_toe)
        self.tic_tac_toe.make_move(square, 'O')
        self.update_board()
        winner = self.tic_tac_toe.current_winner
        if winner:
            messagebox.showinfo("Game Over", f"{winner} wins!")
            self.root.quit()
        elif not self.tic_tac_toe.empty_squares():
            messagebox.showinfo("Game Over", "It's a tie!")
            self.root.quit()
        else:
            self.current_player = 'X'

if __name__ == '__main__':
    root = tk.Tk()
    ttt_gui = TicTacToeGUI(root)
    root.mainloop()
