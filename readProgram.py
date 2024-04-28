import ctypes as ct
import sys
from typing import Optional

COLUMNSIZE = 19
NUMCOLUMNS = 8
HFLIB = ct.CDLL("lib/hackFreecell.dll")

class readProgram:
    def get_game_number(self) -> int:
        temp = (ct.c_ubyte * 5)()
        result = HFLIB.get_game_number(temp)
        if (result == -1):
            print(f'Error getting game board')
            return -1
        ret = ''
        for b in temp:
            if b == 0:
                break
            ret += chr(b)
        ret = int(ret)
        return ret
    
    def get_freecells(self) -> Optional[list[str]]:
        'Edits the given board to fill it with the freecells. The return value is 0 on success, -1 on failure'
        temp = (ct.c_ubyte * 4)()
        result = HFLIB.get_freecells(temp)
        if (result == -1):
            return None
        board = list()
        for i in range(4):
            pos = hex(temp[i])[2:]
            if len(pos) < 2:
                pos = '0' + pos
            pos = pos.upper()
            board.append(pos)
        return board

    def get_foundations(self) -> Optional[list[list[str]]]:
        'Edits the given board to fill it with the foundations. The return value is 0 on success, -1 on failure'
        temp = (ct.c_ubyte * 4)()
        result = HFLIB.get_foundations(temp)
        if (result == -1):
            return None
        board = list()
        for i in range(4):
            to_add = list()
            if temp[i] != 255:
                start = temp[i] % 4
                for j in range(start, temp[i]+1, 4):
                    pos = hex(j)[2:]
                    if len(pos) < 2:
                        pos = '0' + pos
                    pos = pos.upper()
                    to_add.append(pos)
            board.append(to_add.copy())
        return board

    def get_tableau(self) -> Optional[list[str]]:
        'Edits the given board to fill it with the tableau. The return value is 0 on success, -1 on failure'
        temp = (ct.c_ubyte * (NUMCOLUMNS*COLUMNSIZE))()
        result = HFLIB.get_tableau(temp)
        if (result == -1):
            return None
        board = list()
        for i in range(NUMCOLUMNS):
            to_add = list()
            for j in range(COLUMNSIZE):
                curr_index = (i*COLUMNSIZE)+j
                if temp[curr_index] == 255:
                    break
                to_add.append(temp[curr_index])
            board.append(to_add.copy())
        return board

def main():

    rp = readProgram()

    freecells = rp.get_freecells()
    if not freecells:
        print(f'Failed getting freecells')
        return 1
    
    foundations = rp.get_foundations()
    if not foundations:
        print(f'Error getting foundations')
        return 1

    tableau = rp.get_tableau()
    if not tableau:
        print(f'Error getting tableau')
        return 1

    print(f'The freecells are {freecells}')
    print(f'The foundations are {foundations}')
    print(f'The tableau is')
    for c in tableau:
        print(c)

    return 0

if __name__ == '__main__':
    sys.exit(main())