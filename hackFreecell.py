import ctypes as ct

test = ct.c_char_p(b'erm')
print(test.value)