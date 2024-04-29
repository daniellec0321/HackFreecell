import sys
import subprocess
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

def generate_moves(data: str):
    'Dont know what it should return yet'
    pass

def main():
    rp = readProgram()
    board = rp.get_tableau()
    new = convertBoard(board)
    data = create_solver(new)

if __name__ == '__main__':
    sys.exit(main())