import sys
import subprocess
import time
from typing import Optional
from readProgram import readProgram
rp = readProgram()

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
    for idx, s in enumerate(states):
        print(f'{idx}: {s}')
    return [moves, states]

def gameLoop(moves: list[tuple[str, int, str]], states: list[tuple[list[list[int]], list[int], list[int]]]) -> int:

    # Print initial move
    board = rp.get_tableau()
    cells = rp.get_freecells()
    foundations = sorted(rp.get_foundations())
    initial_state = (tuple(tuple(col) for col in board), tuple(cells), tuple(foundations))
    try:
        move_index = states.index(initial_state)
    except ValueError:
        print(f'Could not find the game state. Please restart the game and the solver.')
        return -1
    
    src, num, dst = moves[move_index]
    print(f'src is {src}, num is {num}, dst is {dst}')
    src_type = 'column'
    dst_type = 'column'
    if src[0] == 'F':
        src_type = 'freecell'
    if dst[0] == 'F':
        dst_type = 'freecell'
    elif dst[0] == 'P':
        dst_type = 'foundations'
    if dst_type == 'foundations':
        print(f'Move {num} cards from {src_type} {src[1:]} to the foundations')
    else:
        print(f'Move {num} cards from {src_type} {src[1:]} to {dst_type} {dst[1:]}')
    
    while (sorted(foundations) != [48, 49, 50, 51]):
        # Get the new game state
        new_board = rp.get_tableau()
        new_cells = rp.get_freecells()
        new_foundations = sorted(rp.get_foundations())
        if (new_board == board) and (cells == new_cells) and (foundations == new_foundations):
            time.sleep(0.25)
            continue
        state = (tuple(tuple(col) for col in new_board), tuple(new_cells), tuple(new_foundations))
        print(f'Current game state: {state}')
        try:
            move_index = states.index(state)
        except ValueError:
            # print(f'Could not find the game state. Please restart the game and the solver.')
            # Try sleeping for 1 second then reading again
            time.sleep(1)
            new_board = rp.get_tableau()
            new_cells = rp.get_freecells()
            new_foundations = sorted(rp.get_foundations())
            state = (tuple(tuple(col) for col in new_board), tuple(new_cells), tuple(new_foundations))
            if state not in states:
                print(f'Could not find the game state. Please restart the game and the solver.')
                return -1
            move_index = states.index(state)
        src, num, dst = moves[move_index]
        print(f'src is {src}, num is {num}, dst is {dst}')
        src_type = 'column'
        dst_type = 'column'
        if src[0] == 'F':
            src_type = 'freecell'
        if dst[0] == 'F':
            dst_type = 'freecell'
        elif dst[0] == 'P':
            dst_type = 'foundations'
        if dst_type == 'foundations':
            print(f'Move {num} cards from {src_type} {src[1:]} to the foundations')
        else:
            print(f'Move {num} cards from {src_type} {src[1:]} to {dst_type} {dst[1:]}')
        board = [col.copy() for col in new_board.copy()]
        cells = new_cells.copy()
        foundations = new_foundations.copy()

    return 0

def main():
    board = rp.get_tableau() # returns list[list[int]]
    new = convertBoard(board) # new is [list[list[str]]]
    data = create_solver(new)
    ret = generate_moves(board, data)
    if not ret:
        print('Game is unsolveable.')
        return 1
    moves, states = ret
    
    status = gameLoop(moves, states)

    return 0

if __name__ == '__main__':
    sys.exit(main())