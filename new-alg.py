#!/usr/bin/env python3


import sys
import heapq
from readProgram import readProgram
from typing import Optional

numCalls = 0

ACES = ["00", "01", "02", "03"]

def myFind(l: list, n) -> int:
    try:
        ret = l.index(n)
        return ret
    except ValueError:
        return -1

def print_game_state(board: list[list[str]], free_cells: list[str], foundations: list[list[str]]):
    print(f'Foundations: {[c[-1] for c in foundations if c]}')
    print(f'Freecells: {free_cells}')
    for c in board:
        print(c)

def find_score(board: list[list[str]], free_cells: list[str], foundations: list[list[str]]) -> int:
    # -2 for every card in the freecells, +2 for every card in the foundation
    score = 0
    # score -= (len(list(filter(lambda l: l != 'FF', free_cells)))) * 2
    erm = False
    for card in map(lambda l: int(l, 16), filter(lambda l: l != 'FF', free_cells)):
        erm = True
        # Find cards 'above' it
        cards_above = [card+5, card+6] # Default clubs
        if 48 <= card <= 51: #If the cards are kings
            cards_above = [255, 255]
        elif card % 4 == 1: #diamond
            cards_above = [card+3, card+6]
        elif card % 4 == 2: #heart
            cards_above = [card+2, card+5]
        elif card % 4 == 3:
            cards_above = [card+2, card+3]
        # Find where card is on the board
        for col in board:
            thing = list(map(lambda l: int(l, 16), list(reversed(col.copy()))))
            val1 = myFind(thing, cards_above[0])
            val2 = myFind(thing, cards_above[1])
            print(f'for card {hex(card)}, {val1}, {val2}')
            if (val1 != -1 and val2 != -1):
                score -= min(val1, val2)
            elif val1 != -1:
                score -= val1
            elif val2 != -1:
                score -= val2
            else:
                score -= 10
            break
    if erm:
        print(f'Freecells : {free_cells}')
        print(f'Foundations: {foundations}')
        print(f'Board')
        for c in board:
            print(c)
        print(f'The score (no foundations) is {score}')
        sys.exit(0)
    score += (sum(map(len, foundations))) * 3
    
    # smaller and larger columns are better than medium_sized columns
    all_lens = list(map(len, board))
    avg = sum(all_lens) / 8
    score += sum(map(lambda l: abs(l-avg), all_lens))
    return score


def make_move(orig_board, orig_free_cells, orig_foundations, move):
    
    src, dest = move

    # Making changes on copies
    board = [col.copy() for col in orig_board]
    free_cells = orig_free_cells.copy()
    foundations = [foundation.copy() for foundation in orig_foundations]

    # Moving from column to free cell
    if dest[0] == "F" and src[0] == "C":
        free_index = int(dest[1])
        src = int(src[1])
        if board[src]:
            free_cells[free_index] = board[src].pop()

    # Moving from free cell to column
    elif src[0] == "F" and dest[0] == "C":
        dest = int(dest[1])
        free_index = int(src[1])
        board[dest].append(free_cells[free_index])
        free_cells[free_index] = "FF"

    # Move from Freecell to foundation
    elif src[0] == "F" and dest[0] == "P":
        dest = int(dest[1])
        free_index = int(src[1])
        foundations[dest].append(free_cells[free_index])
        free_cells[free_index] = "FF"


    # Moving from column to foundation
    elif dest[0] == "P" and src[0] == "C":
        foundation_index = int(dest[1])
        src = int(src[1])
        if board[src]:
            card = board[src].pop()
            foundations[foundation_index].append(card)

    # Moving within columns
    elif dest[0] == "C" and src[0] == "C":
        dest_col = int(dest[1])
        src = int(src[1])
        if board[src]:
            board[dest_col].append(board[src].pop())

    return board, free_cells, foundations


def generate_moves(board, free_cells, foundations):
    
    moves = []

    # Move that move from/to a column preceed with C
    # Moves that move from/to a free cell preceed with F
    # Moves that move from/to a foundation pile preceed with P



    # Move from columns to foundations
    for col_index, col in enumerate(board):
        if col:  # Check if column is not empty
            card = col[-1]
            for f_index, foundation in enumerate(foundations):
                if (not foundation and card in ACES) or \
                        (foundation and int(foundation[-1], 16)%4 == int(card,16)%4 and int(card, 16) == int(foundation[-1], 16) + 4):
                    new_move = ("C{}".format(col_index), "P{}".format(f_index))
                    temp_board, temp_free, temp_found = make_move(board, free_cells, foundations, new_move)
                    score = find_score(temp_board, temp_free, temp_found)
                    heapq.heappush(moves, (score*-1, new_move))
                    # moves.append(("C{}".format(col_index), "P{}".format(f_index)))


    # Move from freecells to foundations
    for free_col_index, card in enumerate(free_cells):
        if card == "FF":
            continue
        for f_index, foundation in enumerate(foundations):
            if (not foundation and card in ACES) or \
                    (foundation and int(foundation[-1], 16)%4 == int(card,16)%4 and int(card, 16) == int(foundation[-1], 16) + 4):
                new_move = ("F{}".format(free_col_index), "P{}".format(f_index))
                temp_board, temp_free, temp_found = make_move(board, free_cells, foundations, new_move)
                score = find_score(temp_board, temp_free, temp_found)
                heapq.heappush(moves, (score*-1, new_move))
                # moves.append(("F{}".format(free_col_index), "P{}".format(f_index)))

    # Move within columns
    for src_col_index, src_col in enumerate(board):
        if src_col:  # Check if column is not empty
            for dest_col_index, dest_col in enumerate(board):
                if src_col_index != dest_col_index:
                    if not dest_col or (((int(dest_col[-1],16)%4 == 0 and int(src_col[-1],16)%4 == 1) or \
                                        (int(dest_col[-1],16)%4 == 0 and int(src_col[-1],16)%4 == 2) or \
                                        (int(dest_col[-1],16)%4 == 1 and int(src_col[-1],16)%4 == 0) or \
                                        (int(dest_col[-1],16)%4 == 1 and int(src_col[-1],16)%4 == 3) or \
                                        (int(dest_col[-1],16)%4 == 2 and int(src_col[-1],16)%4 == 0) or \
                                        (int(dest_col[-1],16)%4 == 2 and int(src_col[-1],16)%4 == 0) or \
                                        (int(dest_col[-1],16)%4 == 3 and int(src_col[-1],16)%4 == 1) or \
                                        (int(dest_col[-1],16)%4 == 3 and int(src_col[-1],16)%4 == 2)) and \
                                        (int(dest_col[-1], 16)//4 - 1 ==  int(src_col[-1],16)//4)):
                        new_move = ("C{}".format(src_col_index), "C{}".format(dest_col_index))
                        temp_board, temp_free, temp_found = make_move(board, free_cells, foundations, new_move)
                        score = find_score(temp_board, temp_free, temp_found)
                        heapq.heappush(moves, (score*-1, new_move))
                        # moves.append(("C{}".format(src_col_index), "C{}".format(dest_col_index)))

    # Move from columns to free cells
    for col_index, col in enumerate(board):
        if col:
            for free_index, free_cell in enumerate(free_cells):
                if free_cell == "FF":  # Empty free cell
                    new_move = ("C{}".format(col_index), "F{}".format(free_index))
                    temp_board, temp_free, temp_found = make_move(board, free_cells, foundations, new_move)
                    score = find_score(temp_board, temp_free, temp_found)
                    heapq.heappush(moves, (score*-1, new_move))
                    # moves.append(("C{}".format(col_index), "F{}".format(free_index)))
                    break

    # Move from free cells to columns
    for free_col_index, free_col in enumerate(free_cells):
            if free_col == "FF":
                continue
            for dest_col_index, dest_col in enumerate(board):                                           # below if statements check they are alternating black and red for suits
                if not dest_col or (((int(dest_col[-1],16)%4 == 0 and int(free_col[-1],16)%4 == 1) or \
                                        (int(dest_col[-1],16)%4 == 0 and int(free_col[-1],16)%4 == 2) or \
                                        (int(dest_col[-1],16)%4 == 1 and int(free_col[-1],16)%4 == 0) or \
                                        (int(dest_col[-1],16)%4 == 1 and int(free_col[-1],16)%4 == 3) or \
                                        (int(dest_col[-1],16)%4 == 2 and int(free_col[-1],16)%4 == 0) or \
                                        (int(dest_col[-1],16)%4 == 2 and int(free_col[-1],16)%4 == 0) or \
                                        (int(dest_col[-1],16)%4 == 3 and int(free_col[-1],16)%4 == 1) or \
                                        (int(dest_col[-1],16)%4 == 3 and int(free_col[-1],16)%4 == 2)) and \
                                        (int(dest_col[-1], 16)//4 - 1 == int(free_col[-1], 16)//4)):      # check that its one number lower
                        new_move = ("F{}".format(free_col_index), "C{}".format(dest_col_index))
                        temp_board, temp_free, temp_found = make_move(board, free_cells, foundations, new_move)
                        score = find_score(temp_board, temp_free, temp_found)
                        heapq.heappush(moves, (score*-1, new_move))
                        # moves.append(("F{}".format(free_col_index), "C{}".format(dest_col_index)))

        

    return moves

def solve_freecell(board: list[list[str]], cells: list[str], foundations: list[list[str]], visited: Optional[set], moves: Optional[list[tuple]], depth: int=0) -> list[bool, Optional[list[list[str]]], Optional[list[str]], Optional[list[list[str]]], Optional[set], Optional[list[tuple]]]:

    global numCalls
    numCalls += 1
    # print(f'Numcalls is {numCalls}')
    
    # Check if this is a winning game state
    if len(list(filter(lambda l: len(l) != 13, foundations))) == 0:
        return [True, board, cells, foundations, visited, moves]

    # Don't want to bother exploring this node, so just return everything
    if depth >= 6:
        return [False, board, cells, foundations, visited, moves]
    
    if not visited:
        visited = set()
    if not moves:
        moves = list()

    board_state = (tuple(tuple(col) for col in board), tuple(cells), tuple(tuple(col) for col in foundations))
    if board_state in visited:
        return [False, None, None, None, None, None]
    visited.add(board_state)

    possible_moves = generate_moves(board, cells, foundations)
    if not possible_moves:
        [False, None, None, None, None, None]

    best_score = -1 * sys.maxsize
    best_board = None
    best_freecells = None
    best_foundations = None
    best_moves = None
    best_visited = None
    if len(possible_moves) == 0:
        print(f'Freecells: {cells}')
        print(f'Foundations: {foundations}')
        print(f'Board:')
        for c in board:
            print(c)
        print(f'No possible moves')
    for _, move in possible_moves[:9]:
        temp_board, temp_cells, temp_foundations = make_move(board, cells, foundations, move)
        temp_moves = moves.copy()
        temp_moves.append(move)
        status, new_board, new_cells, new_foundations, new_visited, new_moves = solve_freecell(temp_board, temp_cells, temp_foundations, visited, temp_moves, depth+1)
        if status:
            return [status, new_board, new_cells, new_foundations, new_visited, new_moves]
        if not new_board:
            continue
        new_score = find_score(new_board, new_cells, new_foundations)
        # Update best score
        if new_score > best_score:
            best_score = new_score
            best_board = [col.copy() for col in new_board]
            best_freecells = new_cells.copy()
            best_foundations = [col.copy() for col in new_foundations]
            best_visited = new_visited.copy()
            best_moves = new_moves.copy()
    
    if best_board:
        return [False, best_board, best_freecells, best_foundations, best_visited, best_moves]
    return [False, None, None, None, None, None]

def helper(board: list[list[str]], cells: list[str], foundations: list[list[str]], visited: Optional[set], moves: Optional[list[tuple]]) -> Optional[list[tuple]]:

    temp_board = [col.copy() for col in board]
    temp_cells = cells.copy()
    temp_foundations = [col.copy() for col in foundations]
    temp_visited = None
    if visited:
        temp_visited = visited.copy()
    temp_moves = None
    if moves:
        temp_moves = moves.copy()
    sol_found = False
    it = 0
    while not sol_found:
        it += 1
        sol_found, temp_board, temp_cells, temp_foundations, temp_visited, temp_moves = solve_freecell(temp_board, temp_cells, temp_foundations, temp_visited, temp_moves)
        if sol_found:
            return temp_moves
        # No possible solution at all
        if not temp_board:
            return None



def main():

    rp = readProgram()

    # freecells = ['FF', 'FF', 'FF', 'FF']
    # foundations = [[], ['01'], [], []]
    # board = [
    #     ["17", "1B", "1A", "25", "00", "05", "0B"],
    #     ["1F", "08", "01", "02", "2C", "2E", "09"],
    #     ["0D", "12", "0F", "1C", "07", "14", "32"],
    #     ["2D", "27", "15", "22", "1E", "0C", "16"],
    #     ["20", "26", "13", "31", "18", "04"],
    #     ["10", "29", "0E", "1D", "0A", "24"],
    #     ["00", "19", "11", "2F", "06", "2B"],
    #     ["21", "2A", "28", "30", "33", "23"]
    # ]
    # print(f'the score is {find_score(board, freecells, foundations)}')

    ''' 
    initial_board = [
        ["00"],
        ["03", "06", "0B"],
        ["02", "07"],
        ["01", "04","0A"], [],[],[],[]]
    print(initial_board)
    '''
     
    # initial_board = [
    #     ["17", "1B", "1A", "25", "00", "05", "0B"],
    #     ["1F", "08", "01", "02", "2C", "2E", "09"],
    #     ["0D", "12", "0F", "1C", "07", "14", "32"],
    #     ["2D", "27", "15", "22", "1E", "0C", "16"],
    #     ["20", "26", "13", "31", "18", "04"],
    #     ["10", "29", "0E", "1D", "0A", "24"],
    #     ["00", "19", "11", "2F", "06", "2B"],
    #     ["21", "2A", "28", "30", "33", "23"]
    # ]
    # initial_board = [
    #     ["33"], ["32"], ["31"], [], [], [], [], []
    # ]
    
    '''
    initial_board = [
        ["17", "1B", "1A", "25", "00", "05", "0B", "FF", "FF", "FF", "FF", "FF", "FF"],
        ["1F", "08", "01", "02", "2C", "2E", "09", "FF", "FF", "FF", "FF", "FF", "FF"],
        ["0D", "12", "0F", "1C", "07", "14", "32", "FF", "FF", "FF", "FF", "FF", "FF"],
        ["2D", "27", "15", "22", "1E", "0C", "16", "FF", "FF", "FF", "FF", "FF", "FF"],
        ["20", "26", "13", "31", "18", "04", "FF", "FF", "FF", "FF", "FF", "FF", "FF"],
        ["10", "29", "0E", "1D", "0A", "24", "FF", "FF", "FF", "FF", "FF", "FF", "FF"],
        ["00", "19", "11", "2F", "06", "2B", "FF", "FF", "FF", "FF", "FF", "FF", "FF"],
        ["21", "2A", "28", "30", "33", "23", "FF", "FF", "FF", "FF", "FF", "FF", "FF"]
    ]
    '''

    # initial_board = [
    #     ["06", "05", "04", "03", "02", "01", "00"],
    #     ["0D", "0C", "0B", "0A", "09", "08", "07"],
    #     ["14", "13", "12", "11", "10", "0F", "0E"],
    #     ["1B", "1A", "19", "18", "17", "16", "15"],
    #     ["21", "20", "1F", "1E", "1D", "1C"],
    #     ["27", "26", "25", "24", "23", "22"],
    #     ["2D", "2C", "2B", "2A", "29", "28"],
    #     ["33", "32", "31", "30", "2F", "2E"]
    # ]

    # initial_free_cells = ["FF", "FF", "FF", "FF"]
    
    # initial_foundations = [[],[],[],[]]
    # initial_foundations = [
    #     ["00", "04", "08", "0C", "10", "14", "18", "1C", "20", "24", "28", "2C", "30"],
    #     ["01", "05", "09", "0D", "11", "15", "19", "1D", "21", "25", "29", "2D"],
    #     ["02", "06", "0A", "0E", "12", "16", "1A", "1E", "22", "26", "2A", "2E"],
    #     ["03", "07", "0B", "0F", "13", "17", "1B", "1F", "23", "27", "2B", "2F"]
    # ]

    initial_board = rp.get_tableau()
    if not initial_board:
        print(f'Error getting game data')
        return 1
    initial_free_cells = rp.get_freecells()
    if not initial_free_cells:
        print(f'Error getting game data')
        return 1
    initial_foundations = rp.get_foundations()
    if not initial_foundations:
        print(f'Error getting game data')
        return 1

    initial_score = find_score(initial_board, initial_free_cells, initial_foundations)
    # solved, final_board, move_list = solve_freecell(initial_board, initial_free_cells, initial_foundations, 0, initial_score)
    # solved, final_board, final_freecells, final_foundations, move_list = solve_freecell(initial_board, initial_free_cells, initial_foundations, None, None, 0)
    move_list = helper(initial_board, initial_free_cells, initial_foundations, None, None)

    if move_list:
        print("Solution found! Moves:")
        for temp in move_list:
            move = temp[1]
            print(temp)
        # print("\nFinal Board:")
        # for col in final_board:
        #     print(col)
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()





'''
Hex values of cards
FF: No card
00: Ace of clubs
01: Ace of diamonds
02: Ace of hearts
03: Ace of spades
04: 2 of clubs
05: 2 of diamonds
06: 2 of hearts
07: 2 of spades
08: 3 of clubs
09: 3 of diamonds
0A: 3 of hearts
0B: 3 of spades
0C: 4 of clubs
0D: 4 of diamonds
0E: 4 of hearts
0F: 4 of spades
10: 5 of clubs
11: 5 of diamonds
12: 5 of hearts
13: 5 of spades
14: 6 of clubs
15: 6 of diamonds
16: 6 of hearts
17: 6 of spades
18: 7 of clubs
19: 7 of diamonds
1A: 7 of hearts
1B: 7 of spades
1C: 8 of clubs
1D: 8 of diamonds
1E: 8 of hearts
1F: 8 of spades
20: 9 of clubs
21: 9 of diamonds
22: 9 of hearts
23: 9 of spades
24: 10 of clubs
25: 10 of diamonds
26: 10 of hearts
27: 10 of spades
28: Jack of clubs
29: Jack of diamonds
2A: Jack of hearts
2B: Jack of spades
2C: Queen of clubs
2D: Queen of diamonds
2E: Queen of hearts
2F: Queen of spades
30: King of clubs
31: King of diamonds
32: King of hearts
33: King of spades

'''
