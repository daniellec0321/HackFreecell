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
        self.totalMoves = -1
        self.root = None
        self.move_text = None

    def inc_move(self):
        if self.lastMove < self.totalMoves:
            self.lastMove += 1

    def dec_move(self):
        if self.lastMove > 0:
            self.lastMove -= 1

    def get_move(self) -> int:
        'Return the move index and the move.'
        # THERE IS NO LOOP IN HERE
        # run this every 0.1 seconds
        # Get the next move, by comparing the given game state and last move
        win = False
        board = rp.get_tableau()
        cells = rp.get_freecells()
        foundations = sorted(rp.get_foundations())
        if foundations == [48, 49, 50, 51]:
            self.move_text['text'] = 'You Win!'
            return 0
        else:
            if self.lastMove == -1:
                # Get initial state
                # board = rp.get_tableau()
                # cells = rp.get_freecells()
                # foundations = sorted(rp.get_foundations())
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
                # board = rp.get_tableau()
                # cells = rp.get_freecells()
                # foundations = sorted(rp.get_foundations())
                if foundations == [48, 49, 50, 51]:
                    win = True
                state = (tuple(tuple(col) for col in board), tuple(cells), tuple(foundations))
                if self.curr_state != state:
                    indices = [i for i, x in enumerate(self.states) if x == state]
                    found = False
                    for i in indices:
                        if i > self.lastMove:
                            self.lastMove = i
                            found = True
                            break
                    self.curr_state = state
                self.curr_move = self.moves[self.lastMove]
            # Set the label
            num_cards = self.curr_move[1]
            src_type = 'column'
            src = self.curr_move[0][1]
            if self.curr_move[0][0] == 'F':
                src_type = 'freecell'
            dst_type = 'column'
            dst = self.curr_move[2][1]
            if self.curr_move[2][0] == 'F':
                dst_type = 'freecell'
            elif self.curr_move[2][0] == 'P':
                dst_type = 'the'
                dst = 'foundations'
            if num_cards == 1:
                text = f'Step {self.lastMove+1} out of {self.totalMoves}: Move {num_cards} card from {src_type} {src} to {dst_type} {dst}'
            else:
                text = f'Step {self.lastMove+1} out of {self.totalMoves}: Move {num_cards} cards from {src_type} {src} to {dst_type} {dst}'
            self.move_text['text'] = text
        self.root.after(100, self.get_move) # run itself again after 1000 ms
        return 0

    def loop(self) -> int:
        # initialize the moves and states
        board = rp.get_tableau() # returns list[list[int]]
        if not board:
            print(f'Failure to get the game board.')
            return -1
        if not all(map(lambda l: len(l) == 7, board[:4])) or not all(map(lambda l: len(l) == 6, board[4:])):
            print('Board is corrupted. Make sure you have a new game ready and set.')
            return -1
        cells = rp.get_freecells()
        foundations = rp.get_foundations()
        if cells != [255, 255, 255, 255] or foundations != [255, 255, 255, 255]:
            print('Freecells and/or foundations are corrupted. Make sure you have a new game ready and set.')
            return -1
        new = erm.convertBoard(board) # new is [list[list[str]]]
        data = erm.create_solver(new)
        ret = erm.generate_moves(board, data)
        if not ret:
            print('Game is unsolveable.')
            return 1
        self.moves, self.states = ret
        self.totalMoves = len(self.moves)

        self.root = tk.Tk()
        canvas = tk.Canvas(self.root, width=500, height=300)
        canvas.grid(columnspan=3, rowspan=4)
        canvas.create_text(250, 25, text='FreeCell Move Generator', font=('Helvetica', 16, 'bold'))

        self.move_text = tk.Label(self.root, text='', font=('Helvetica', 10))
        self.move_text.grid(column=1, row=3)

        move_label = tk.StringVar()
        move_btn = tk.Button(self.root, textvariable=move_label, command=lambda:self.inc_move(), height=2, width=15)
        move_label.set("Next Move")
        move_btn.grid(column=1, row=1)
        back_label = tk.StringVar()
        back_btn = tk.Button(self.root, textvariable=back_label, command=lambda:self.dec_move(), height=2, width=15)
        back_label.set("Last Move")
        back_btn.grid(column=1, row=2)
        status = self.get_move()

        self.root.mainloop()
        return status

def main() -> int:
    s = Solver()
    status = s.loop()
    # if status == -1:
    #     return 1
    # return 0
    return status == -1

if __name__ == '__main__':
    sys.exit(main())