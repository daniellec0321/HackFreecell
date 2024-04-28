import sys
import requests
from readProgram import readProgram

def get_solution(game_num: int) -> list[tuple[str, str], str]:
    'Reads the game number and returns the moves as a list of tuples'
    url = f'https://freecellgamesolutions.com/ds/?g={game_num}&v=All'
    r = requests.get(url)
    data = r.text
    data = data.split('auto moves to home</tr>')[1]
    to_read = data.split("adsbygoogle")
    for section in to_read:
        if '<tr>' not in section:
            continue
        print(f'------------')
        print(section)

def main():
    rp = readProgram()

    game_num = rp.get_game_number()
    if game_num == -1:
        return 1
    get_solution(game_num)
    return 0

if __name__ == '__main__':
    sys.exit(main())