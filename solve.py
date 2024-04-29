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

def generate_moves(data: str) -> Optional[list[str]]:
    'Dont know what it should return yet'
    if 'I could not solve this game' in data:
        return None
    return ['erm']

def main():
    rp = readProgram()
    board = rp.get_tableau()
    print(board)
    new = convertBoard(board)
    data = create_solver(new)
    moves = generate_moves(data)
    if not moves:
        print('Game is unsolveable.')
        return 1
    return 0

if __name__ == '__main__':
    sys.exit(main())