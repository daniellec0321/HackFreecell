import sys
from readProgram import readProgram
from solve import Solve
rp = readProgram()
s = Solve()

board = rp.get_tableau() # returns list[list[int]]
new = s.convertBoard(board) # new is [list[list[str]]]
data = s.create_solver(new)
ret = s.generate_moves(board, data)
if not ret:
    print('Game is unsolveable.')
    sys.exit(1)
moves, states = ret

move_num, move = s.guiLoop(moves, states)
while move:
    print(move)
    move = s.guiLoop(moves, states)

sys.exit(0)