import tkinter as tk
import sys
from readProgram import readProgram
from solve import Solve
rp = readProgram()
erm = Solve()

class Solver:

    def __init__(self):
        self.moves = list()
        self.states = list()
        self.curr_state = tuple()
        self.curr_move = tuple()
        self.lastMove = -1
        self.root = None
        self.move_text = None

    def inc_move(self):
        self.lastMove += 1

    def get_move(self):
        'Return the move index and the move.'
        # THERE IS NO LOOP IN HERE
        # run this every 0.1 seconds
        # Get the next move, by comparing the given game state and last move
        if self.lastMove == -1:
            # Get initial state
            board = rp.get_tableau()
            cells = rp.get_freecells()
            foundations = rp.get_foundations()
            state = (tuple(tuple(col) for col in board), tuple(cells), tuple(foundations))
            self.curr_state = state
            indices = [i for i, x in enumerate(self.states) if x == state]
            for i in indices:
                if i > self.lastMove:
                    self.lastMove = i
                    break
            if self.lastMove == -1:
                self.lastMove = 0
            self.curr_move = self.moves[self.lastMove]
        else:
            board = rp.get_tableau()
            cells = rp.get_freecells()
            foundations = rp.get_foundations()
            state = (tuple(tuple(col) for col in board), tuple(cells), tuple(foundations))
            if self.curr_state != state:
                indices = [i for i, x in enumerate(self.states) if x == state]
                found = False
                for i in indices:
                    if i > self.lastMove:
                        self.lastMove = i
                        found = True
                        break
                if found == True:
                    print(f'git here hmmm')
                # if temp == self.lastMove: # Could not find the move
                #     temp = self.lastMove
                self.curr_state = state
            self.curr_move = self.moves[self.lastMove]
        # Set the label
        self.move_text['text'] = f'{self.lastMove}: {self.curr_move}'
        self.root.after(100, self.get_move) # run itself again after 1000 ms

    def loop(self):
        # initialize the moves and states
        board = rp.get_tableau() # returns list[list[int]]
        new = erm.convertBoard(board) # new is [list[list[str]]]
        data = erm.create_solver(new)
        ret = erm.generate_moves(board, data)
        if not ret:
            print('Game is unsolveable.')
            return 1
        self.moves, self.states = ret

        self.root = tk.Tk()
        canvas = tk.Canvas(self.root, width=500, height=300)
        canvas.grid(columnspan=3, rowspan=3)
        canvas.create_text(250, 25, text='FreeCell Move Generator', font=('Helvetica', 16, 'bold'))

        self.move_text = tk.Label(self.root, text='', font=('Helvetica', 10))
        self.move_text.grid(column=1, row=2)

        move_label = tk.StringVar()
        move_btn = tk.Button(self.root, textvariable=move_label, command=lambda:self.inc_move(), height=2, width=15)
        move_label.set("Next Move")
        move_btn.grid(column=1, row=1)
        self.get_move()

        self.root.mainloop()

def main():
    s = Solver()
    s.loop()

if __name__ == '__main__':
    main()