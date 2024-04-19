from tkinter import *
from tkinter import ttk
import os
import sys
from tkinter.ttk import Style

#Mainframe
root = Tk()
root.title("Server Builder")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.geometry("250x80")
#root.iconbitmap("icon.ico")


for Arg in sys.argv:
    print(Arg)
    if "-developer=true" == Arg:
        developer_mode = True
    else:
        developer_mode = False

def setup_server():
    root.destroy()
    os.system(f"python3 ./GUISetupServer.py -developer={str(developer_mode).lower()}")

def launch_server():
    root.destroy()
    os.system(f"python3 ./GUILaunchServer.py -developer={str(developer_mode).lower()}")

ttk.Button(mainframe, text="Launch-Server", command=launch_server).grid(column=0, row=0, sticky=W)
ttk.Button(mainframe, text="Setup-Server", command=setup_server).grid(column=0, row=1, sticky=W)

root.mainloop()

input("Press Enter to exit...")

