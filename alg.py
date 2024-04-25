#!/usr/bin/env python3


import sys
import heapq
import skeleton 

sys.setrecursionlimit(10000)

ACES = ["00", "01", "02", "03"]

def find_score(board: list[list[str]], free_cells: list[str], foundations: list[list[str]]) -> int:
    # -1 for every card in the freecells, +2 for every card in the foundation
    score = 0
    score -= len(list(filter(lambda l: l != 'FF', free_cells)))
    score += (sum(map(len, foundations))) * 2
    
    # smaller and larger columns are better than medium_sized columns
    all_lens = list(map(len, board))
    avg = sum(all_lens) / 8
    score += sum(map(lambda l: abs(l-avg), all_lens))
    return score


def make_move(board, free_cells, move, foundations):
    
    src, dest = move

    # Making changes on copies
    board = [col.copy() for col in board]
    free_cells = free_cells.copy()
    foundations = [foundation.copy() for foundation in foundations]

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
                    temp_board, temp_free, temp_found = make_move(board, free_cells, new_move, foundations)
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
                temp_board, temp_free, temp_found = make_move(board, free_cells, new_move, foundations)
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
                        temp_board, temp_free, temp_found = make_move(board, free_cells, new_move, foundations)
                        score = find_score(temp_board, temp_free, temp_found)
                        heapq.heappush(moves, (score*-1, new_move))
                        # moves.append(("C{}".format(src_col_index), "C{}".format(dest_col_index)))

    # Move from columns to free cells
    for col_index, col in enumerate(board):
        if col:
            for free_index, free_cell in enumerate(free_cells):
                if free_cell == "FF":  # Empty free cell
                    new_move = ("C{}".format(col_index), "F{}".format(free_index))
                    temp_board, temp_free, temp_found = make_move(board, free_cells, new_move, foundations)
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
                        temp_board, temp_free, temp_found = make_move(board, free_cells, new_move, foundations)
                        score = find_score(temp_board, temp_free, temp_found)
                        heapq.heappush(moves, (score*-1, new_move))
                        # moves.append(("F{}".format(free_col_index), "C{}".format(dest_col_index)))

        

    return moves


def solve_freecell(board, free_cells, foundations, visited_states=None, moves=None, depth=0):
    
    # Initialize visited_states and moves if not provided. Visited States just stores a bunch of past boards
    if visited_states is None:
        visited_states = set()

    if moves is None:
        moves = []

    # Convert the board state to a tuple for hashing
    board_state = tuple(tuple(col) for col in board)

    # Base Case: If all columns are empty, the game is solved
    if all(not col for col in board) and all(free == "FF" for free in free_cells):
        return True, board, moves

    # Check if we've already visited this state
    if board_state in visited_states:
        # print("Return 2")
        return False, None, None

    visited_states.add(board_state)
    # Recursive Step: Generate all possible moves. Possible_moves is frontier
    possible_moves = generate_moves(board, free_cells, foundations)
    # print(board_state)
    # print(possible_moves)
    # print()
    if not possible_moves:
        # print("Return 3")
        return False, None, None

    for temp in possible_moves:
        move = temp[1]

        # for col in board:
        #     print(f"{'    ' * depth}{col}")
        # print(f"{'    ' * depth}Current Free Cells: {free_cells}")
        
        # print(f"{'    ' * depth}Current Foundations Cells: {foundations}")

        print(f"{'    ' * depth}Trying Move: {move}")
        new_board, new_free_cells, new_foundations = make_move(board.copy(), free_cells.copy(), move, foundations.copy())
        
        # print(f"{'    ' * depth}New Board State:")
        # for col in new_board:
        #     print(f"{'    ' * depth}{col}")
        # print(f"{'    ' * depth}New Free Cells: {new_free_cells}")

        # print(f"{'    ' * depth}New Foundations Cells: {new_foundations}")
        
        # print()
    
        # Recurse and explore this move
        solved, result_board, move_list = solve_freecell(new_board, new_free_cells, new_foundations, visited_states, moves + [move])

        if solved:
            # print("Return 4")
            return True, result_board, move_list
    # print("Return 5")
    return False, None, None


def main():

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
    initial_board = [
        ["17", "1B", "1A", "25", "00", "05", "0B"],
        ["1F", "08", "01", "02", "2C", "2E", "09"],
        ["0D", "12", "0F", "1C", "07", "14", "32"],
        ["2D", "27", "15", "22", "1E", "0C", "16"],
        ["20", "26", "13", "31", "18", "04"],
        ["10", "29", "0E", "1D", "0A", "24"],
        ["03", "19", "11", "2F", "06", "2B"],
        ["21", "2A", "28", "30", "33", "23"]
        ["33"], ["32"], ["31"], [], [], [], [], []
    ]
    
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
    initial_free_cells = ["FF", "FF", "FF", "FF"]
    
    # initial_foundations = [[],[],[],[]]
    initial_foundations = [
        ["00", "04", "08", "0C", "10", "14", "18", "1C", "20", "24", "28", "2C", "30"],
        ["01", "05", "09", "0D", "11", "15", "19", "1D", "21", "25", "29", "2D"],
        ["02", "06", "0A", "0E", "12", "16", "1A", "1E", "22", "26", "2A", "2E"],
        ["03", "07", "0B", "0F", "13", "17", "1B", "1F", "23", "27", "2B", "2F"]
    ]

    solved, final_board, move_list = solve_freecell(initial_board, initial_free_cells, initial_foundations)

    if solved:
        print("Solution found! Moves:")
        for temp in move_list:
            move = temp[1]
            print(move)
        print("\nFinal Board:")
        for col in final_board:
            print(col)
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
