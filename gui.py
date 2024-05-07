import sys
from threading import Thread
import time
import tkinter as tk
from readProgram import readProgram
rp = readProgram()
from solve import Move

class GUI:

    def __init__(self):
        self.Move = Move()
        self.root = None
        self.move_text = None
        self.visited = set()
        self.done = False

    def tracker(self):
        try:
            while True:
                if self.done:
                    break
                board = rp.get_tableau()
                cells = rp.get_freecells()
                foundations = rp.get_foundations()
                if not board or not cells or not foundations:
                    self.visited = set()
                else:
                    state = self.Move.make_game_state(board, cells, foundations)
                    self.visited.add(state)
                time.sleep(0.25)
        except:
            return

    def make_text(self, moves: list[tuple[str, int, str]]) -> str:
        text = ''
        for move in moves:
            if move[0][0] == 'C' and move[2][0] == 'C':
                if move[1] == 1:
                    text += f'Move a card from column {move[0][1]} to column {move[2][1]}\n'
                else:
                    text += f'Move {move[1]} cards from column {move[0][1]} to column {move[2][1]}\n'
            elif move[0][0] == 'C' and move[2][0] == 'F':
                text += f'Move a card from column {move[0][1]} to freecell {move[2][1]}\n'
            elif move[0][0] == 'C' and move[2][0] == 'P':
                text += f'Move a card from column {move[0][1]} to the foundations\n'
            elif move[0][0] == 'F' and move[2][0] == 'C':
                text += f'Move a card from freecell {move[0][1]} to column {move[2][1]}\n'
        return text

    def inc_move(self):
        board = rp.get_tableau()
        if not board:
            self.move_text['text'] = '\n\n\n\n\n'
            self.visited = set()
            return
        cells = rp.get_freecells()
        if not cells:
            self.move_text['text'] = '\n\n\n\n\n'
            self.visited = set()
            return
        foundations = rp.get_foundations()
        if not foundations:
            self.move_text['text'] = '\n\n\n\n\n'
            self.visited = set()
            return
        state = self.Move.make_game_state(board, cells, foundations)
        self.visited.add(state)
        moves = self.Move.get_move(board, cells, foundations, self.visited)
        self.move_text['text'] = self.make_text(moves)

    def loop(self):
        self.root = tk.Tk()
        canvas = tk.Canvas(self.root, width=500, height=300)
        canvas.grid(columnspan=3, rowspan=3)
        canvas.create_text(250, 25, text='FreeCell Move Generator', font=('Helvetica', 16, 'bold'))
        self.move_text = tk.Label(self.root, text='', font=('Helvetica', 10))
        self.move_text.grid(column=1, row=2)
        self.move_text['text'] = '\n\n\n\n\n'
        move_label = tk.StringVar()
        move_btn = tk.Button(self.root, textvariable=move_label, command=lambda: self.inc_move(), height=2, width=15)
        move_label.set("Generate moves...")
        move_btn.grid(column=1, row=1)
        t1 = Thread(target=self.tracker)
        try:
            t1.start()
            self.root.mainloop()
        except:
            pass
        self.done = True
        t1.join()

def main() -> int:
    g = GUI()
    g.loop()
    return 0

if __name__ == '__main__':
    sys.exit(main())