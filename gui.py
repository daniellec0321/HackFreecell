import sys
import subprocess
from typing import Optional
import tkinter as tk
from readProgram import readProgram
rp = readProgram()

class Solver:

    def __init__(self):
        self.moves = list()
        self.states = list()
        self.curr_state = tuple()
        self.curr_move = tuple()
        self.mode = 'Automatic'
        self.lastMove = -1
        self.totalMoves = -1
        self.root = None
        self.move_text = None

    def inc_move(self):
        if self.lastMove < self.totalMoves:
            self.mode = 'Manual'
            self.lastMove += 1

    def dec_move(self):
        if self.lastMove > 0:
            self.mode = 'Manual'
            self.lastMove -= 1

    def convertBoard(self, board: list[list[int]]) -> list[list[str]]:
        'Convert board to something the executable can read'
        ret = list()
        for row in board:
            to_add = list()
            for card in row:
                num = str(int(card / 4) + 1)
                if num == '1':
                    num = 'A'
                elif num == '11':
                    num = 'J'
                elif num == '12':
                    num = 'Q'
                elif num == '13':
                    num = 'K'
                suit = card % 4
                if suit == 0:
                    suit = 'C'
                elif suit == 1:
                    suit = 'D'
                elif suit == 2:
                    suit = 'H'
                else:
                    suit = 'S'
                new_card = num + suit
                to_add.append(new_card)
            ret.append(to_add.copy())
        return ret
    
    def create_solver(self, board: list[list[str]]) -> str:
        # Create the moves
        f = open('temp.txt', 'w')
        for row in board:
            for card in row:
                f.write(card)
                f.write(' ')
            f.write('\n')
        f.close()
        f = open("moves.txt", "w")
        subprocess.run(["./fc-solve.exe", "-m", "temp.txt"], stdout=f)
        f.close()
        subprocess.run(["rm", "temp.txt"])
        # Read the moves into memory
        f = open("moves.txt", "r")
        data = f.read()
        f.close()
        subprocess.run(["rm", "moves.txt"])
        return data
    
    def generate_moves(self, board: list[list[int]], data: str) -> Optional[list[list[tuple[str, int, str]], list[tuple[list[list[int]], list[int], list[int]]]]]:
        'Dont know what it should return yet'
        if 'I could not solve this game' in data:
            return None
        moves = list()
        states = list()
        initial_freecells = [255, 255, 255, 255]
        initial_foundations = [255, 255, 255, 255]
        initial_state = (tuple(tuple(col) for col in board), tuple(initial_freecells), tuple(initial_foundations))
        states.append(initial_state)

        curr_board = [col.copy() for col in board.copy()]
        curr_cells = initial_freecells.copy()
        curr_foundations = initial_foundations.copy()
        # Loop through lines of data
        for line in filter(lambda l: 'Move' in l, data.split('\n')):
            move_src = ''
            move_card = 1
            move_dst = ''
            words = line.split()
            if words[1] != 'a': # Moving within columns
                num_cards_to_move = int(words[1])
                src = int(words[5])
                dst = int(words[8])
                cards_to_move = curr_board[src][-1*num_cards_to_move:].copy()
                for card in cards_to_move:
                    curr_board[dst].append(card)
                for _ in range(num_cards_to_move):
                    curr_board[src].pop()
                move_src = 'C' + str(src)
                move_card = num_cards_to_move
                move_dst = 'C' + str(dst)
            else:
                src_type = words[4]
                if src_type == 'stack':
                    src = int(words[5])
                    dst_type = words[7]
                    move_src = 'C' + str(src)
                    card = curr_board[src].pop()
                    if dst_type == 'freecell':
                        dst = int(words[8])
                        curr_cells[dst] = card
                        move_dst = 'F' + str(dst)
                    elif dst_type == 'the': # foundations
                        # Find the correct stack
                        dst = -1
                        for i in range(4):
                            cf = curr_foundations[i]
                            if (cf != 255) and ((cf%4) == (card%4)):
                                dst = i
                                break
                        if dst == -1:
                            dst = curr_foundations.index(255)
                        curr_foundations[dst] = card
                        move_dst = 'P' + str(dst)
                    else:
                        print('Issue reading data.')
                        return None
                elif src_type == 'freecell':
                    src = int(words[5])
                    dst_type = words[7]
                    move_src = 'F' + str(src)
                    card = curr_cells[src]
                    curr_cells[src] = 255
                    if dst_type == 'stack':
                        dst = int(words[8])
                        curr_board[dst].append(card)
                        move_dst = 'C' + str(dst)
                    elif dst_type == 'the':
                        dst = -1
                        for i in range(4):
                            cf = curr_foundations[i]
                            if (cf != 255) and ((cf%4) == (card%4)):
                                dst = i
                                break
                        if dst == -1:
                            dst = curr_foundations.index(255)
                        curr_foundations[dst] = card
                        move_dst = 'P' + str(dst)
                    else:
                        print('Issue reading data.')
                        return None
                else:
                    print('Issue reading data.')
                    return None
            # Add the move and state
            moves.append((move_src, move_card, move_dst))
            state_to_add = (tuple(tuple(col) for col in curr_board), tuple(curr_cells), tuple(sorted(curr_foundations)))
            states.append(state_to_add)
        return [moves, states]

    def get_move(self) -> int:
        'Return the move index and the move.'
        # THERE IS NO LOOP IN HERE
        # run this every 0.1 seconds
        # Get the next move, by comparing the given game state and last move
        mode = 'Manual'
        win = False
        board = rp.get_tableau()
        cells = rp.get_freecells()
        foundations = rp.get_foundations()
        if not board or not cells or not foundations:
            self.move_text['text'] = 'Could not read game data.'
            return -1
        elif sorted(foundations) == [48, 49, 50, 51]:
            self.move_text['text'] = 'You Win!'
            return 0
        else:
            foundations = sorted(foundations)
            if self.lastMove == -1:
                state = (tuple(tuple(col) for col in board), tuple(cells), tuple(foundations))
                self.curr_state = state
                indices = [i for i, x in enumerate(self.states) if x == state]
                for i in indices:
                    if i > self.lastMove:
                        self.mode = 'Automatic'
                        self.lastMove = i
                        break
                if self.lastMove == -1:
                    self.lastMove = 0
                self.curr_move = self.moves[self.lastMove]
            else:
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
                            self.mode = 'Automatic'
                            break
                    if not found:
                        self.mode = 'Manual'
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
                text = f'{self.mode} mode\nStep {self.lastMove+1} out of {self.totalMoves}: Move {num_cards} card from {src_type} {src} to {dst_type} {dst}'
            else:
                text = f'{self.mode} mode\nStep {self.lastMove+1} out of {self.totalMoves}: Move {num_cards} cards from {src_type} {src} to {dst_type} {dst}'
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
        new = self.convertBoard(board)
        data = self.create_solver(new)
        ret = self.generate_moves(board, data)
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
    return status == -1

if __name__ == '__main__':
    sys.exit(main())