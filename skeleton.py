import ctypes as ct
import sys

COLUMNSIZE = 19
NUMCOLUMNS = 8
HFLIB = ct.CDLL("lib/hackFreecell.dll")

def get_freecells(board: list[int]) -> bool:
    'Edits the given board to fill it with the freecells. The return value is 0 on success, -1 on failure'
    temp = (ct.c_ubyte * 4)()
    result = HFLIB.get_freecells(temp)
    if (result == -1):
        return False
    for i in range(4):
        board[i] = temp[i]
    return True

def get_foundations(board: list[int]) -> bool:
    'Edits the given board to fill it with the foundations. The return value is 0 on success, -1 on failure'
    temp = (ct.c_ubyte * 4)()
    result = HFLIB.get_foundations(temp)
    if (result == -1):
        return False
    for i in range(4):
        board[i] = temp[i]
    return True

def get_tableau(board: list[list[int]]) -> bool:
    'Edits the given board to fill it with the tableau. The return value is 0 on success, -1 on failure'
    temp = (ct.c_ubyte * (NUMCOLUMNS*COLUMNSIZE))()
    result = HFLIB.get_tableau(temp)
    if (result == -1):
        return False
    for i in range(NUMCOLUMNS):
        for j in range(COLUMNSIZE):
            board[i][j] = temp[(i*COLUMNSIZE)+j]
    return True

def main():

    freecells = [0, 0, 0, 0]
    if (not get_freecells(freecells)):
        print('Failed getting the freecells')
        return 1
    foundations = [0, 0, 0, 0]
    if (not get_foundations(foundations)):
        print('Failed getting the foundations')
        return 1

    tableau = list()
    for i in range(NUMCOLUMNS):
        l = list()
        for j in range(COLUMNSIZE):
            l.append(0)
        tableau.append(l.copy())
    if (not get_tableau(tableau)):
        print('Failed getting the tableau')
        return 1

    print(f'The freecells are {list(map(lambda l: hex(l), freecells))}')
    print(f'The foundations are {list(map(lambda l: hex(l), foundations))}')
    print(f'The tableau is')
    for c in tableau:
        print(list(map(lambda l: hex(l), c)))

    return 0

if __name__ == '__main__':
    sys.exit(main())