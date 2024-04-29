#!/usr/bin/env python3

import tkinter as tk

moves = [('C1', 2, 'C3'), ('F1', 0, 'C4'), ('C2', 0, 'F1'), ('C2', 0,'P2')]

root = tk.Tk()
canvas = tk.Canvas(root, width=500, height=300)
canvas.grid(columnspan=3, rowspan=3)
canvas.create_text(250, 25, text='FreeCell Move Generator', font=('Helvetica', 16, 'bold'))

move_text = tk.Label(root, text='', font=('Helvetica', 10))
move_text.grid(column=1, row=2)

def next_move():
    if moves:
        src, cards, dest = moves.pop(0)
        match src[0]:
            case 'C':
                num = 0
                if cards > 1:
                    num = cards
                    text = 'Move '+str(num)+' cards from column '+src[1]+' to '
                else:
                    num = 1
                    text = 'Move '+str(num)+' card from column '+src[1]+' to '
            case 'F':
                text = 'Move 1 card from freecell '+src[1]+' to '
        match dest[0]:
            case 'C':
                text += 'column '+dest[1]
            case 'F':
                text += 'freecell '+dest[1]
            case 'P':
                text += 'foundation pile '+dest[1]
    else:
        text = 'No moves remaining.'
    move_text['text'] = text

move_label = tk.StringVar()
move_btn = tk.Button(root, textvariable=move_label, command=lambda:next_move(), height=2, width=15)
move_label.set("Next Move")
move_btn.grid(column=1, row=1)

root.mainloop()