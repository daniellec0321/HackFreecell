import sys
import subprocess
from typing import Optional
from readProgram import readProgram

def convertBoard(board: list[list[int]]) -> list[list[str]]:
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

def create_solver(board: list[list[str]]) -> str:
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

def generate_moves(board: list[list[int]], data: str) -> Optional[list[list[tuple[str, int, str]], list[tuple[list[list[int]], list[int], list[int]]]]]:
    'Dont know what it should return yet'
    if 'I could not solve this game' in data:
        return None
    moves = list()
    states = list()
    initial_freecells = [-1, -1, -1, -1]
    initial_foundations = [-1, -1, -1, -1]
    initial_state = (tuple(tuple(col) for col in board), tuple(initial_freecells), tuple(initial_foundations))
    states.append(initial_state)

    curr_board = [col.copy() for col in board.copy()]
    print(curr_board)
    curr_cells = initial_freecells.copy()
    curr_foundations = initial_foundations.copy()
    # Loop through lines of data
    for line in filter(lambda l: 'Move' in l, data.split('\n')):
        print(line)
        move_src = ''
        move_card = 0
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
                    dst = 0
                    for i in range(4):
                        if (curr_foundations[i] != -1) and (int(curr_foundations[i]/4) == (int(card/4)+1)):
                            dst = i
                            break
                    curr_foundations[dst] = card
                    move_dst = 'P' + str(dst)
                else:
                    print('what2')
                    return None
            elif src_type == 'freecell':
                src = int(words[5])
                dst_type = words[7]
                move_src = 'F' + str(src)
                card = curr_cells[src]
                curr_cells[src] = -1
                if dst_type == 'stack':
                    dst = int(words[8])
                    curr_board[dst].append(card)
                    move_dst = 'C' + str(dst)
                elif dst_type == 'the':
                    dst = 0
                    for i in range(4):
                        if (curr_foundations[i] != -1) and (int(curr_foundations[i]/4) == (int(card/4)+1)):
                            dst = i
                            break
                    curr_foundations[dst] = card
                    move_dst = 'P' + str(dst)
                else:
                    print('what3')
                    return 1
            else:
                print('what')
                return None
        # Add the move and state
        moves.append((move_src, move_card, move_dst))
        print(f'the move is {(move_src, move_card, move_dst)}')
        stop = input('...')
        state_to_add = (tuple(tuple(col) for col in curr_board), tuple(curr_cells), tuple(curr_foundations))
        states.append(state_to_add)
    return [moves, states]

def main():
    rp = readProgram()
    board = rp.get_tableau() # returns list[list[int]]
    new = convertBoard(board) # new is [list[list[str]]]
    data = create_solver(new)
    ret = generate_moves(board, data)
    if not ret:
        print('Game is unsolveable.')
        return 1
    moves, states = ret
    return 0

if __name__ == '__main__':
    sys.exit(main())