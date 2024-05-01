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

    def generate_moves(self, board: list[list[int]], cells: list[int], foundations: list[int]) -> list[tuple[str, int, str]]:
        moves = list()
        # Column to column
        can_move = self.max_cards_to_move(board, cells)
        for idx, col in enumerate(board):
            print(f'Analyzing col {idx}...')
            for i in range(len(col)-1, -1, -1):
                if len(col[i:]) > can_move:
                    break
                if not self.cards_in_order(col[i:]):
                    break
                print(f'Checking this subcolumn: {col[i:]}')
                for j, c in enumerate(board):
                    if j == idx:
                        continue
                    if not c and len(col[i:]) != can_move: # Empty column
                        moves.append(("C"+str(j), len(col[i:]), "C"+str(idx)))
                        continue
                    # Check if src card can go on this dst
                    if int(col[i]/4) != int(c[-1]/4)-1:
                        print(f'col[i] is {hex(col[i])}, c[-1] is {hex(c[-1])}. Wrong number')
                        continue
                    if self.get_color(col[i]) == self.get_color(c[-1]):
                        print(f'col[i] is {hex(col[i])}, c[-1] is {hex(c[-1])}. Wrong color')
                        continue
                    print(f'col[i] is {hex(col[i])}, c[-1] is {hex(c[-1])}. We\'re good!')
                    moves.append(("C"+str(j), len(col[i:]), "C"+str(idx)))
        # Column to freecell
        # Column to foundations
        # Freecell to column
        # Freecell to foundations
        return moves


    def get_move(self, board: list[list[int]], cells: list[int], foundations: list[int]):
        pass

if __name__ == '__main__':
    rp = readProgram()
    m = Move()
    board = rp.get_tableau()
    cells = rp.get_freecells()
    foundations = rp.get_foundations()
    print(m.generate_moves(board, cells, foundations))