#!/usr/bin/env python3


import sys

ACES = ["00", "01", "02", "03"]

def make_move(board, free_cells, move, foundations):
    
    src, dest = move

    # Making changes on copies
    board = [col.copy() for col in board]
    free_cells = free_cells.copy()

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

    return board, free_cells


def generate_moves(board, free_cells, foundations):
    
    moves = []

    # Move from columns to free cells
    for col_index, col in enumerate(board):
        for free_index, free_cell in enumerate(free_cells):
            if free_cell == "FF":  # Empty free cell
                moves.append(("C{}".format(col_index), "F{}".format(free_index)))

    # Move from free cells to columns
    for free_col_index, free_col in enumerate(free_cells):
            if free_col == "FF":
                continue
            for dest_col_index, dest_col in enumerate(board):
                if not dest_col or (((int(dest_col[-1],16)%4 == 0 and int(free_col[-1],16)%4 == 1) or \
                                        (int(dest_col[-1],16)%4 == 0 and int(free_col[-1],16)%4 == 2) or \
                                        (int(dest_col[-1],16)%4 == 1 and int(free_col[-1],16)%4 == 0) or \
                                        (int(dest_col[-1],16)%4 == 1 and int(free_col[-1],16)%4 == 3) or \
                                        (int(dest_col[-1],16)%4 == 2 and int(free_col[-1],16)%4 == 0) or \
                                        (int(dest_col[-1],16)%4 == 2 and int(free_col[-1],16)%4 == 0) or \
                                        (int(dest_col[-1],16)%4 == 3 and int(free_col[-1],16)%4 == 1) or \
                                        (int(dest_col[-1],16)%4 == 3 and int(free_col[-1],16)%4 == 2)) and \
                                        int(dest_col[-1], 16) == int(free_col[-1], 16) - 4):
                        moves.append(("F{}".format(free_col_index), "C{}".format(dest_col_index)))

    # Move from freecells to foundations
    for free_col_index, card in enumerate(free_cells):
        if card == "FF":
            continue
        for f_index, foundation in enumerate(foundations):
            if (not foundation and card in ACES) or \
                    (foundation and int(foundation[-1], 16)%4 == int(card,16)%4 and int(card[0], 16) == int(foundation[-1], 16) + 4):
                moves.append(("F{}".format(free_col_index), "P{}".format(f_index)))
        
        
    # Move from columns to foundations
    for col_index, col in enumerate(board):
        if col:  # Check if column is not empty
            card = col[-1]
            for f_index, foundation in enumerate(foundations):
                if (not foundation and card in ACES) or \
                        (foundation and int(foundation[-1], 16)%4 == int(card,16)%4 and int(card[0], 16) == int(foundation[-1], 16) + 4):
                    moves.append(("C{}".format(col_index), "P{}".format(f_index)))

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
                                        int(dest_col[-1], 16) == int(src_col[-1], 16) - 4):
                        moves.append(("C{}".format(src_col_index), "C{}".format(dest_col_index)))

    return moves


def solve_freecell(board, free_cells, foundations, visited_states=None, moves=None):
    
    # Initialize visited_states and moves if not provided. Visited States just stores a bunch of past boards
    if visited_states is None:
        visited_states = set()

    if moves is None:
        moves = []

    # Convert the board state to a tuple for hashing
    board_state = tuple(tuple(col) for col in board)

    # Base Case: If all columns are empty, the game is solved
    if all(not col for col in board):
        return True, board, moves

    # Check if we've already visited this state
    if board_state in visited_states:
        return False, None, None

    visited_states.add(board_state)

    # Recursive Step: Generate all possible moves. Possible_moves is frontier
    possible_moves = generate_moves(board, free_cells, foundations)

    if not possible_moves:
        return False, None, None

    for move in possible_moves:
        new_board, new_free_cells = make_move(board.copy(), free_cells.copy(), move, foundations.copy())

        # Recurse and explore this move
        solved, result_board, move_list = solve_freecell(new_board, new_free_cells, foundations, visited_states, moves + [move])

        if solved:
            return True, result_board, move_list

    return False, None, None


def main():
    initial_board = [
        ["17", "1B", "1A", "25", "00", "05", "0B"],
        ["1F", "08", "01", "02", "2C", "2E", "09"],
        ["0D", "12", "0F", "1C", "07", "14", "32"],
        ["2D", "27", "15", "22", "1E", "0C", "16"],
        ["20", "26", "13", "31", "18", "04"],
        ["10", "29", "0E", "1D", "0A", "24"],
        ["00", "19", "11", "2F", "06", "2B"],
        ["21", "2A", "28", "30", "33", "23"]
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
    
    initial_foundations = [[],[],[],[]]

    solved, final_board, move_list = solve_freecell(initial_board, initial_free_cells, initial_foundations)

    if solved:
        print("Solution found! Moves:")
        for move in move_list:
            print(move)
        print("\nFinal Board:")
        for col in final_board:
            print(col)
    else:
        print("No solution found.")

if __name__ == "__main__":
    main()
