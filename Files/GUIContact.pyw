#Imports
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import Listbox
from tkinter import filedialog
from tkinter import DISABLED
from tkinter import NORMAL
from tkinter import BooleanVar
from Functions import no_feature, exit, do_you_like_to_continue_afterbuild, server_launching, no_selection
import sys
import os
import time
from tkinter.ttk import Style
from tkinter import Tk, PhotoImage
import subprocess
import ctypes

if __name__ == "__main__":   
    if 'win' in sys.platform:
        ctypes.windll.shcore.SetProcessDpiAwareness(1)

#Mainframe
root = Tk()
root.title("Contact")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.geometry("275x70")
icon_image = PhotoImage(file="icon.png")
root.wm_iconphoto(True, icon_image)

def back():
    root.destroy()
    subprocess.Popen(["pythonw", "GUISettings.pyw"])
    
def create_buttons():
    ttk.Button(mainframe, text="Back", command=back).grid(column=0, row=0, sticky=W)

def text_gui():
    window_text = ttk.Label(mainframe, text="Discord Server : https://discord.gg/t4mYGbErAn")
    window_text.grid(column=0, row=1, sticky=W)
    window_text = ttk.Label(mainframe, text="Discord Message : @wfxey, @iv32.")
    window_text.grid(column=0, row=2, sticky=W)

#Starting Mainloop
create_buttons()

text_gui()

root.mainloop()

input("Press Enter to exit...")