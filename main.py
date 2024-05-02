import tkinter as tk
from tkinter import ttk, simpledialog

from game.sudoku import Sudoku
from interface.config import CANVAS_WIDTH, CANVAS_HEIGHT, ROWS, COLS, SQUARE_SIZE, PADDING


class AppInterface:
    def __init__(self):
        self._root = tk.Tk()
        self._difficult = None
        self._sudoku = None

        self._root.title("Game SUDOKU")
        self._canvas = tk.Canvas(self._root, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        self._canvas.pack()

        self.build_grid_empty()
        self.append_botao_fechar()
        self.append_botao_reset()
        self.show_difficult()

        self._canvas.bind("<Button-1>", self.handle_click_wrapper)

        self._root.mainloop()

    def build_grid_empty(self):
        for row in range(ROWS):
            for col in range(COLS):
                x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                self.draw_square_empty(x, y, SQUARE_SIZE - PADDING, row, col)

    def draw_square_empty(self, x, y, size, row, col):
        x1 = x - size // 2
        y1 = y - size // 2
        x2 = x + size // 2
        y2 = y + size // 2
        quadrado = self._canvas.create_rectangle(x1, y1, x2, y2, outline='black', width=1, tags="square")

        if self._sudoku and self._sudoku.board[row][col] == 0:
            self._canvas.tag_bind(quadrado, "<Button-1>", lambda event, r=row, c=col: self.handle_click(event, r, c))

    def handle_click_wrapper(self, event):
        x, y = event.x, event.y
        col = x // SQUARE_SIZE
        row = y // SQUARE_SIZE

        if self._sudoku and self._sudoku.board[row][col] == 0:
            self.handle_click(event, row, col)

    def handle_click(self, event, row, col):
        num = simpledialog.askinteger("Enter Number", "Enter a number (1-9):", parent=self._root, minvalue=1, maxvalue=9)
        if num is not None:
            is_valid_move = self.validate_board(row,col,num)
            if is_valid_move:
                self._sudoku.board[row][col] = num
                self.fill_numbers()
                if self.check_is_over():
                    tk.messagebox.showinfo("Fim de Jogo","Parabéns Você completou o jogo")
                    self.reset()
            else:
                tk.messagebox.showerror("Erro", "Movimento Inválido")

    def append_botao_fechar(self):
        button_fechar = tk.Button(self._root, text="Sair", command=self.close)
        button_fechar.pack(pady=10)

    def append_botao_reset(self):
        button_reset = tk.Button(self._root, text="Reset", command=self.reset)
        button_reset.pack(padx=10)

    def reset(self):
        self._root.destroy()
        self.__init__()

    def close(self):
        self._root.destroy()

    def get_difficult(self, event):
        option = self._combobox.get()
        self._difficult = option
        self._combobox.destroy()
        self._sudoku = Sudoku(self._difficult)
        self._sudoku.generate()
        self.fill_numbers()

    def fill_numbers(self):
        self._canvas.delete("number")
        if self._sudoku:
            for row in range(ROWS):
                for col in range(COLS):
                    x = col * SQUARE_SIZE + SQUARE_SIZE // 2
                    y = row * SQUARE_SIZE + SQUARE_SIZE // 2
                    number = self._sudoku.board[row][col]
                    if number != 0:
                        self._canvas.create_text(x, y, text=str(number), font=('Arial', 12, 'bold'), tags="number")

    def show_difficult(self):
        selected_option = tk.StringVar()
        combobox = ttk.Combobox(self._root, textvariable=selected_option, values=["Facil", "Medio", "Dificil"], state="readonly")
        combobox.pack(pady=20)
        combobox.bind("<<ComboboxSelected>>", self.get_difficult)
        self._combobox = combobox

    def validate_board(self,row,col,num):
        return self._sudoku.is_valid(row,col,num)

    def check_is_over(self):
        return self._sudoku.is_full()


if __name__ == "__main__":
    app = AppInterface()
