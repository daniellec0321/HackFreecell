import ctypes as ct

freecellLib = ct.CDLL("./lib/hackFreecell.dll")

freecellLib.thing()