import ctypes as ct
import sys

COLUMNSIZE = 19
NUMCOLUMNS = 8
HFLIB = ct.CDLL("lib/hackFreecell.dll")

def get_tableau(board: list[int]) -> bool:
    'Edits the given board to fill it with the tableau. The return value is 0 on success, -1 on failure'
    temp = (ct.c_ubyte * 4)()
    result = HFLIB.get_tableau(temp)
    if (result == -1):
        return False
    for i in range(4):
        board[i] = temp[i]
    return True

def get_stack(board: list[int]) -> bool:
    'Edits the given board to fill it with the stack. The return value is 0 on success, -1 on failure'
    temp = (ct.c_ubyte * 4)()
    result = HFLIB.get_stack(temp)
    if (result == -1):
        return False
    for i in range(4):
        board[i] = temp[i]
    return True

def get_columns(board: list[list[int]]) -> bool:
    'Edits the given board to fill it with the columns. The return value is 0 on success, -1 on failure'
    temp = (ct.c_ubyte * (NUMCOLUMNS*COLUMNSIZE))()
    result = HFLIB.get_columns(temp)
    if (result == -1):
        return False
    for i in range(NUMCOLUMNS):
        for j in range(COLUMNSIZE):
            board[i][j] = temp[(i*COLUMNSIZE)+j]
    return True

def main():
    # Get the tableau
    tableau = [0, 0, 0, 0]
    if (not get_tableau(tableau)):
        print('Failed getting the tableau')
        return 1
    stack = [0, 0, 0, 0]
    if (not get_stack(stack)):
        print('Failed getting the stack')
        return 1
    
    # Have to make this 'columns' list weirdly because of how python copies lists :/
    columns = list()
    for i in range(NUMCOLUMNS):
        l = list()
        for j in range(COLUMNSIZE):
            l.append(0)
        columns.append(l.copy())
    if (not get_columns(columns)):
        print('Failed getting the columns')
        return 1
    
    print(f'The tableau is {tableau}')
    print(f'The stack is {stack}')
    print(f'The columns are')
    for c in columns:
        print(c)

    return 0

if __name__ == '__main__':
    sys.exit(main())