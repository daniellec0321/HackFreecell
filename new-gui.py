import sys
import subprocess
from typing import Optional
import tkinter as tk
from readProgram import readProgram
rp = readProgram()
from solve import Move

def loop(self) -> int:
    status = 0
    # Get moves

    self.root = tk.Tk()
    canvas = tk.Canvas(self.root, width=500, height=300)
    # canvas.grid(columnspan=3, rowspan=4)
    canvas.grid(columnspan=3, rowspan=3)
    canvas.create_text(250, 25, text='FreeCell Move Generator', font=('Helvetica', 16, 'bold'))

    self.move_text = tk.Label(self.root, text='', font=('Helvetica', 10))
    # self.move_text.grid(column=1, row=3)
    self.move_text.grid(column=1, row=2)
    move_label = tk.StringVar()
    move_btn = tk.Button(self.root, textvariable=move_label, command=lambda:self.inc_move(), height=2, width=15)
    move_label.set("Generate moves...")
    move_btn.grid(column=1, row=1)
    status = self.get_move()

    self.root.mainloop()
    return status

def main() -> int:
    status = loop
    return status == -1

if __name__ == '__main__':
    sys.exit(main())