import requests
import ctypes as ct
HFLIB = ct.CDLL("lib/hackFreecell.dll")

def get_game_number() -> int:
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

def main():
    test = get_game_number()
    return 0

if __name__ == '__main__':
    main()