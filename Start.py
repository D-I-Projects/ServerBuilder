from tkinter import *
from tkinter import ttk
from Functions import no_feature
import os
import sys

root = Tk()
mainframe = ttk.Frame(root, padding="2 1 12 12")
root.title("Menue")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))


for Arg in sys.argv:
    print(Arg)
    if "-developer=true" == Arg:
        developer_mode = True
    else:
        developer_mode = False

def setup_server():
    root.destroy()
    os.system(f"python3 ./GUI.py -developer={str(developer_mode).lower()}")

ttk.Button(mainframe, text="Launch-Server", command=no_feature).grid(column=1, row=1, sticky=W)
ttk.Button(mainframe, text="Setup-Server", command=setup_server).grid(column=3, row=1, sticky=W)

root.mainloop()

