import sys
from typing import Optional
from readProgram import readProgram

class Move:

    def max_cards_to_move(self, board: list[list[int]], cells: list[int]) -> int:
        can_move = 1
        can_move += len(list(filter(lambda l: l == 255, cells)))
        can_move += len(list(filter(lambda l: l == [], board)))
        return can_move

    def get_color(self, card: int) -> str:
        if card % 4 == 1 or card % 4 == 2:
            return 'red'
        return 'black'

    def cards_in_order(self, col: list[int]) -> bool:
        for i in range(len(col)-1):
            # Wrong number
            if int(col[i]/4) != int(col[i+1]/4)+1:
                return False
            if self.get_color(col[i]) == self.get_color(col[i+1]):
                return False
        return True
    
    def get_score(cells: list[int], foundations: list[int]) -> int:
        score = 0
        score += sum(list(filter(lambda l: l != 255, foundations)))
        score -= len(list(filter(lambda l: l != 255, cells))) * 2
        return score

    def generate_moves(self, board: list[list[int]], cells: list[int], foundations: list[int]) -> Optional[list[tuple[str, int, str]]]:
        moves = list()
        # Column to column
        can_move = self.max_cards_to_move(board, cells)
        for idx, col in enumerate(board):
            for i in range(len(col)-1, -1, -1):
                if len(col[i:]) > can_move:
                    break
                if not self.cards_in_order(col[i:]):
                    break
                for j, c in enumerate(board):
                    if j == idx:
                        continue
                    if not c and len(col[i:]) != can_move: # Empty column
                        moves.append(("C"+str(idx), len(col[i:]), "C"+str(j)))
                        continue
                    if not c and len(col[i:]) == can_move:
                        continue
                    # Check if src card can go on this dst
                    if int(col[i]/4) != int(c[-1]/4)-1:
                        continue
                    if self.get_color(col[i]) == self.get_color(c[-1]):
                        continue
                    moves.append(("C"+str(idx), len(col[i:]), "C"+str(j)))
        # Column to freecell
        freecell = -1
        for i in range(4):
            if cells[i] == 255:
                freecell = i
                break
        if freecell != -1:
            for idx, col in enumerate(board):
                if col:
                    moves.append(("C"+str(idx), 1, "F"+str(freecell)))
        # Column to foundations
        for idx, col in enumerate(board):
            if int(col[-1]/4) == 0: # There's an ace
                freespace = foundations.index(255)
                moves.append(("C"+str(idx), 1, "P"+str(freespace)))
                continue
            card_to_find = col[-1] - 4
            if card_to_find in foundations:
                dest = foundations.index(card_to_find)
                moves.append(("C"+str(idx), 1, "P"+str(dest)))
        # Freecell to column
        for idx, f in enumerate(cells):
            for i, col in enumerate(board):
                if int(f/4) != int(col[-1]/4)-1:
                    continue
                if self.get_color(f) == self.get_color(col[-1]):
                    continue
                moves.append(("F"+str(idx), 1, "C"+str(i)))
        # Freecell to foundations
        for idx, f in enumerate(cells):
            card_to_find = f - 4
            if card_to_find in foundations:
                dest = foundations.index(card_to_find)
                moves.append(("F"+str(idx), 1, "P"+str(dest)))
        return moves
    
    def make_move(self, board: list[list[int]], cells: list[int], foundations: list[int], move: tuple[str, int, str]) -> list[list[list[int]], list[int], list[int]]:
        # Column to column
        new_board = [col.copy() for col in board]
        new_cells = cells.copy()
        new_foundations = foundations.copy()
        if move[0][0] == 'C' and move[2][0] == 'C':
            to_move = board[int(move[0][1])][-1*move[1]:]
            for card in to_move:
                new_board[int(move[2][1])].append(card)
            for _ in range(len(to_move)):
                new_board[int(move[0][1])].pop()
        # Column to cells
        elif move[0][0] == 'C' and move[2][0] == 'F':
            card = new_board[int(move[0][1])].pop()
            new_cells[int(move[2][1])] = card
        # Column to foundations
        elif move[0][0] == 'C' and move[2][0] == 'P':
            card = new_board[int(move[0][1])].pop()
            new_foundations[int(move[2][1])] = card
        # Cells to columns
        elif move[0][0] == 'F' and move[2][0] == 'C':
            card = new_cells[int(move[0][1])]
            new_cells[int(move[0][1])] = 255
            new_board[int(move[2][1])].append(card)
        # Cells to foundations
        else:
            card = new_cells[int(move[0][1])]
            new_cells[int(move[0][1])] = 255
            new_foundations[int(move[2][1])] = card
        return [new_board, new_cells, new_foundations]

    def recurser(self, board: list[list[int]], cells: list[int], foundations: list[int], depth: int) -> int:
        if depth >= 6:
            return -1
        curr_score = self.get_score(cells, foundations)
        moves = self.generate_moves(board, cells, foundations)
        if not moves:
            return -1
        for move in moves:
            # Make the move and recurse
            pass
        pass

    def get_move(board: list[list[int]], cells: list[int], foundations: list[int]) -> Optional[tuple[str, int, str]]:
        pass

def main() -> int:
    rp = readProgram()
    m = Move()
    board = rp.get_tableau()
    cells = rp.get_freecells()
    foundations = rp.get_foundations()
    if not board or not cells or not foundations:
        print(f'Error getting game data')
        return 1
    board = [
        [51, 50, 49, 48, 47, 46, 45],
        [44, 43, 42, 41, 40, 39, 38],
        [37, 36, 35, 34, 33, 32, 31],
        [30, 29, 28, 27, 26, 25, 24],
        [23, 22, 21, 20, 19, 18],
        [17, 16, 15, 14, 13, 12],
        [11, 10, 9, 8, 7, 6],
        [5, 3, 2, 1, 4, 0]
    ]
    foundations = [255, 255, 255, 255]
    cells = [255, 255, 255, 255]
    new_board, new_cells, new_foundations = m.make_move(board, cells, foundations, ("C7", 1, "P0"))
    new_board, new_cells, new_foundations = m.make_move(new_board, new_cells, new_foundations, ("C7", 1, "P0"))
    for row in new_board:
        print(row)
    print(new_cells)
    print(new_foundations)
    return 0

if __name__ == '__main__':
    sys.exit(main())