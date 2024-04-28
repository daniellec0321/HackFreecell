import sys
from readProgram import readProgram

def find_score(board: list[list[int]], free_cells: set[int], foundations: list[int]) -> int:
    # +3 for every card in the foundation, -2 for every card in freecells
    score = 0
    score -= (len(free_cells) * 2)
    score += sum(map(lambda l: int(l/4)+1, filter(lambda l: l != 255, foundations)))
    # smaller and larger columns are better than medium_sized columns
    all_lens = list(map(len, board))
    avg = sum(all_lens) / 8
    score += sum(map(lambda l: abs(l-avg), all_lens))
    return score

def make_move(board: list[list[int]], cells: set[int], foundations: list[int], move: tuple[tuple[str, int], str]) -> list[list[list[str]], set[int], list[int]]:
    'Applies a move to the game board'
    ret_board = [col.copy() for col in board.copy()]
    ret_cells = cells.copy()
    ret_foundations = foundations.copy()
    src, dst = move
    src_pile, src_index = src

    # From freecell to column
    if src_pile[0] == 'F' and dst[0] == 'C':
        card = int(src_pile[1:])
        ret_cells.discard(card) # Delete from freecells
        dst_col = int(dst[1:])
        ret_board[dst_col].append(card)
    # From freecell to foundation
    if src_pile[0] == 'F' and dst[0] == 'P':
        card = int(src_pile[1:])
        ret_cells.discard(card) # Delete from freecells
        dst_col = int(dst[1:])
        ret_foundations[dst_col] = card
    # From column to foundation
    if src_pile[0] == 'C' and dst[0] == 'P':
        src_col = int(src_pile[1:])
        card = ret_board[src_col].pop()
        dst_col = int(dst[1:])
        ret_foundations[dst_col] = card
    # From column to freecell
    if src_pile[0] == 'C' and dst[0] == 'F':
        src_col = int(src_pile[1:])
        card = ret_board[src_col].pop()
        ret_cells.add(card)
    # From column to column
    if src_pile[0] == 'C' and dst[0] == 'C':
        src_col = int(src_pile[1:])
        dst_col = int(dst[1:])
        to_move = ret_board[src_col][src_index:].copy()
        for i in range(len(to_move)):
            ret_board[src_col].pop()
            ret_board[dst_col].append(to_move[i])

    return ret_board, ret_cells, ret_foundations

def helper(board: list[list[int]], free_cells: set[int], foundations: list[int]) -> list[tuple[tuple[str, int], str]]:
    return list()

def main():
    rp = readProgram()

    # Get initial data
    initial_board = rp.get_tableau()
    if not initial_board:
        print(f'Error getting game data')
        return 1
    initial_free_cells = set()
    initial_foundations = [255, 255, 255, 255]
    initial_score = find_score(initial_board, initial_free_cells, initial_foundations)
    print('Initial board')
    print(initial_board)

    # From column to foundation
    # From column to column
    # From column to freecell
    # From freecell to foundation
    # From freecell to column
    move = (("C7", 0), "F")
    new_board, new_cells, new_foundations = make_move(initial_board, initial_free_cells, initial_foundations, move)
    print(new_cells)
    print(new_foundations)
    print(new_board)
    print('-------------------')
    move = (("F21", 0), "C2")
    new_board, new_cells, new_foundations = make_move(new_board, new_cells, new_foundations, move)
    print(new_cells)
    print(new_foundations)
    print(new_board)



if __name__ == '__main__':
    sys.exit(main())