import sys
import subprocess
import time
import msvcrt
from typing import Optional
from readProgram import readProgram
rp = readProgram()

class TimeoutExpired(Exception):
    pass

class Solve:

    def __init__(self):
        self.board = list()
        self.cells = list()
        self.foundations = list()
        self.move = -1

    def input_with_timeout(self, prompt, timeout, timer=time.monotonic):
        sys.stdout.write(prompt)
        sys.stdout.flush()
        endtime = timer() + timeout
        result = []
        while timer() < endtime:
            if msvcrt.kbhit():
                result.append(msvcrt.getwche()) #XXX can it block on multibyte characters?
                if result[-1] == '\r':
                    return ''.join(result[:-1])
            time.sleep(0.04) # just to yield to other processes/threads
        raise TimeoutExpired

    def convertBoard(self, board: list[list[int]]) -> list[list[str]]:
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
    
    def guiLoop(self, moves: list[tuple[str, int, str]], states: list[tuple[list[list[int]], list[int], list[int]]], lastMove: int) -> Optional[list[int, tuple[str, int, str]]]:
        self.board = rp.get_tableau()
        self.cells = rp.get_freecells()
        self.foundations = sorted(rp.get_foundations())
        if lastMove == -1:
            state = (tuple(tuple(col) for col in self.board), tuple(self.cells), tuple(self.foundations))
            indices = [i for i, x in enumerate(states) if x == state]
            move_index = -1
            for i in indices:
                if (i > move_index):
                    move_index = i
                    break
            if move_index == -1:
                print('Error reading game state')
                return None
            self.move = move_index
            return [move_index, moves[move_index]]
        move_index = self.move
        while (sorted(self.foundations) != [48, 49, 50, 51]):
            # Give time for user to force a move
            new_board = rp.get_tableau()
            new_cells = rp.get_freecells()
            new_foundations = sorted(rp.get_foundations())
            if new_foundations == [48, 49, 50, 51]:
                return None
            try:
                _ = self.input_with_timeout('', 0.1)
            except TimeoutExpired:
                if (new_board == self.board) and (self.cells == new_cells) and (self.foundations == new_foundations):
                    time.sleep(0.25)
                    continue
                state = (tuple(tuple(col) for col in new_board), tuple(new_cells), tuple(new_foundations))
                if state not in states:
                    time.sleep(1)
                    new_board = rp.get_tableau()
                    new_cells = rp.get_freecells()
                    new_foundations = sorted(rp.get_foundations())
                    if new_foundations == [48, 49, 50, 51]:
                        return None
                    state = (tuple(tuple(col) for col in new_board), tuple(new_cells), tuple(new_foundations))
                    if state not in states:
                        print(f'Could not find the game state. Playing next move.')
                        move_index += 1
                        # return -1
                    else:
                        indices = [i for i, x in enumerate(states) if x == state]
                        move_index = -1
                        for i in indices:
                            if (i > move_index):
                                move_index = i
                                break
                        if move_index == -1:
                            print('Error reading game state')
                            return None
                else:
                    indices = [i for i, x in enumerate(states) if x == state]
                    move_index = -1
                    for i in indices:
                        if (i > move_index):
                            move_index = i
                            break
                    if move_index == -1:
                        print('Error reading game state')
                        return None
            else:
                move_index += 1
            self.board = [col.copy() for col in new_board.copy()]
            self.cells = new_cells.copy()
            self.foundations = new_foundations.copy()
            self.move = move_index
            return [move_index, moves[move_index]]
            # src, num, dst = moves[move_index]
            # src_type = 'column'
            # dst_type = 'column'
            # if src[0] == 'F':
            #     src_type = 'freecell'
            # if dst[0] == 'F':
            #     dst_type = 'freecell'
            # elif dst[0] == 'P':
            #     dst_type = 'foundations'
            # if dst_type == 'foundations':
            #     print(f'{move_index}: Move {num} cards from {src_type} {src[1:]} to the foundations')
            # else:
            #     print(f'{move_index}: Move {num} cards from {src_type} {src[1:]} to {dst_type} {dst[1:]}')
        return None

    def gameLoop(self, moves: list[tuple[str, int, str]], states: list[tuple[list[list[int]], list[int], list[int]]]) -> int:
        # Print initial move
        board = rp.get_tableau()
        cells = rp.get_freecells()
        foundations = sorted(rp.get_foundations())
        # initial_state = (tuple(tuple(col) for col in board), tuple(cells), tuple(foundations))
        # try:
        #     move_index = states.index(initial_state)
        # except ValueError:
        #     print(f'Could not find the game state. Please restart the game and the solver.')
        #     return -1
        
        # src, num, dst = moves[move_index]
        # src_type = 'column'
        # dst_type = 'column'
        # if src[0] == 'F':
        #     src_type = 'freecell'
        # if dst[0] == 'F':
        #     dst_type = 'freecell'
        # elif dst[0] == 'P':
        #     dst_type = 'foundations'
        # if dst_type == 'foundations':
        #     print(f'Move {num} cards from {src_type} {src[1:]} to the foundations')
        # else:
        #     print(f'Move {num} cards from {src_type} {src[1:]} to {dst_type} {dst[1:]}')
        
        move_index = -1
        while (sorted(foundations) != [48, 49, 50, 51]):
            # Give time for user to force a move
            new_board = rp.get_tableau()
            new_cells = rp.get_freecells()
            new_foundations = sorted(rp.get_foundations())
            if new_foundations == [48, 49, 50, 51]:
                return 0
            try:
                answer = self.input_with_timeout('', 0.1)
            except TimeoutExpired:
                # new_board = rp.get_tableau()
                # new_cells = rp.get_freecells()
                # new_foundations = sorted(rp.get_foundations())
                if (new_board == board) and (cells == new_cells) and (foundations == new_foundations):
                    time.sleep(0.25)
                    continue
                state = (tuple(tuple(col) for col in new_board), tuple(new_cells), tuple(new_foundations))
                # try:
                #     move_index = states.index(state)
                # except ValueError:
                if state not in states:
                    time.sleep(1)
                    new_board = rp.get_tableau()
                    new_cells = rp.get_freecells()
                    new_foundations = sorted(rp.get_foundations())
                    if new_foundations == [48, 49, 50, 51]:
                        return 0
                    state = (tuple(tuple(col) for col in new_board), tuple(new_cells), tuple(new_foundations))
                    if state not in states:
                        print(f'Could not find the game state. Playing next move.')
                        move_index += 1
                        # return -1
                    else:
                        indices = [i for i, x in enumerate(states) if x == state]
                        move_index = -1
                        for i in indices:
                            if (i > move_index):
                                move_index = i
                                break
                        if move_index == -1:
                            print('Error reading game state')
                            return -1
                else:
                    indices = [i for i, x in enumerate(states) if x == state]
                    move_index = -1
                    for i in indices:
                        if (i > move_index):
                            move_index = i
                            break
                    if move_index == -1:
                        print('Error reading game state')
                        return -1
            else:
                move_index += 1
            src, num, dst = moves[move_index]
            src_type = 'column'
            dst_type = 'column'
            if src[0] == 'F':
                src_type = 'freecell'
            if dst[0] == 'F':
                dst_type = 'freecell'
            elif dst[0] == 'P':
                dst_type = 'foundations'
            if dst_type == 'foundations':
                print(f'{move_index}: Move {num} cards from {src_type} {src[1:]} to the foundations')
            else:
                print(f'{move_index}: Move {num} cards from {src_type} {src[1:]} to {dst_type} {dst[1:]}')
            board = [col.copy() for col in new_board.copy()]
            cells = new_cells.copy()
            foundations = new_foundations.copy()

        return 0

def main():
    print('Moves are printed automatically based on your current game board. To forcibly go to the next move, hit Enter.')
    s = Solve()
    board = rp.get_tableau() # returns list[list[int]]
    new = s.convertBoard(board) # new is [list[list[str]]]
    data = s.create_solver(new)
    ret = s.generate_moves(board, data)
    if not ret:
        print('Game is unsolveable.')
        return 1
    moves, states = ret
    
    status = s.gameLoop(moves, states)
    if status == 0:
        print('You Win!')
        return 0
    return 1

if __name__ == '__main__':
    sys.exit(main())