import ctypes as ct

# test = ct.c_char_p(b'erm')
# print(test.value)

hf = ct.CDLL("lib/hackFreecell.dll")
board = (ct.c_ushort * 4)()
test = hf.get_tableau(board)
print(test)
print(f'python board is?')
print(board[1])