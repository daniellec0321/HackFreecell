import ctypes as ct
import sys

hf = ct.CDLL("lib/hackFreecell.dll")

### Getting the tableau
board = (ct.c_ubyte * 4)() # This is the array that you will send to the get_tableau function
result = hf.get_tableau(board) # Get the tableau
if (result == -1):
    print("Error getting the tableau")
    sys.exit(1)
print(f'The board is', end='')
for i in range(4):
    print(f' {hex(board[i])}', end='')
print('')

### Getting the stack
board = (ct.c_ubyte * 4)() # This is the array that you will send to the get_stack function
result = hf.get_stack(board) # Get the stack
if (result == -1):
    print("Error getting the stack")
    sys.exit(1)
print(f'The board is', end='')
for i in range(4):
    print(f' {hex(board[i])}', end='')
print('')