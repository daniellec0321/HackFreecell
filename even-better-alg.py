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

    def get_move(self, board: list[list[int]], cells: list[int], foundations: list[int]):
        pass

def main(args: list[str]) -> int:
    rp = readProgram()
    m = Move()
    board = rp.get_tableau()
    cells = rp.get_freecells()
    foundations = rp.get_foundations()
    if not board or not cells or not foundations:
        print(f'Error getting game data')
        return 1
    moves = m.generate_moves(board, cells, foundations)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))