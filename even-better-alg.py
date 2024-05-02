import sys
from typing import Optional
from readProgram import readProgram

rec = 0

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
    
    def get_score(self, cells: list[int], foundations: list[int]) -> int:
        score = 0
        score += sum(list(filter(lambda l: l != 255, foundations)))
        score -= len(list(filter(lambda l: l != 255, cells))) * 2
        return score
    
    def make_game_state(self, board: list[list[int]], cells: list[int], foundations: list[int]) -> tuple[tuple[tuple[int]], tuple[int], tuple[int]]:
        p1 = tuple(tuple(col) for col in board)
        p2 = tuple(cells)
        p3 = tuple(foundations)
        return (p1, p2, p3)

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
            if not col:
                continue
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
                if not col:
                    moves.append(("F"+str(idx), 1, "C"+str(i)))
                    continue
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

    def recurser(self, board: list[list[int]], cells: list[int], foundations: list[int], visited: set[tuple[tuple[tuple[int]], tuple[int], tuple[int]]], depth: int) -> int:
        # global rec
        # rec += 1
        # print(f'Rec is {rec}')
        # print(f'at depth of {depth}')
        state = self.make_game_state(board, cells, foundations)
        if state in visited:
            # print(f'Got that state is in visited')
            return -1
        # print(f'Past that though!')
        if sorted(foundations) == [48, 49, 50, 51]:
            return sys.maxsize
        if depth >= 5:
            return -1
        visited.add(state)
        best_score = self.get_score(cells, foundations)
        moves = self.generate_moves(board, cells, foundations)
        if not moves:
            return -1
        for move in moves:
            new_board, new_cells, new_foundations = self.make_move(board, cells, foundations, move)
            score = self.recurser(new_board, new_cells, new_foundations, visited, depth+1)
            best_score = max(best_score, score)
        return best_score

    def get_move(self, board: list[list[int]], cells: list[int], foundations: list[int], master_visited: set[tuple[tuple[tuple[int]], tuple[int], tuple[int]]]) -> Optional[tuple[str, int, str]]:
        moves = self.generate_moves(board, cells, foundations)
        if not moves:
            return None
        best_score = -1
        best_move = None
        visited = set()
        for move in moves:
            new_board, new_cells, new_foundations = self.make_move(board, cells, foundations, move)
            # Send this to recurser (if needed)
            state = self.make_game_state(new_board, new_cells, new_foundations)
            if state in master_visited:
                continue
            score = self.recurser(new_board, new_cells, new_foundations, visited, 0)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def game_loop(self):
        rp = readProgram()
        visited = set()
        while True:
            board = rp.get_tableau()
            cells = rp.get_freecells()
            foundations = rp.get_foundations()
            if not board or not cells or not foundations:
                print(f'Error getting game data')
                return
            state = self.make_game_state(board, cells, foundations)
            # print(board)
            # print(cells)
            # print(foundations)
            visited.add(state)
            move = self.get_move(board, cells, foundations, visited)
            if not move:
                print('Cannot make a move!!!')
            else:
                print(move)
            stop = input('stopping...')

def main() -> int:
    # rp = readProgram()
    # m = Move()
    # board = rp.get_tableau()
    # cells = rp.get_freecells()
    # foundations = rp.get_foundations()
    # if not board or not cells or not foundations:
    #     print(f'Error getting game data')
    #     return 1
    m = Move()
    m.game_loop()
    return 0

if __name__ == '__main__':
    sys.exit(main())