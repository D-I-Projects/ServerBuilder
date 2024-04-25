#Imports
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import Listbox
from tkinter import filedialog
from tkinter import DISABLED
from tkinter import NORMAL
from tkinter import BooleanVar
from Functions import no_feature, exit, do_you_like_to_continue_afterbuild, do_you_like_to_continue_only_if_installed_serverjar, server_launching, accepting_eula
import sys
import os
import time
from tkinter.ttk import Style
import subprocess

# Mainframe
root = Tk()
root.title("Launch Server")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.geometry("250x70")
icon_image = PhotoImage(file="icon.png")
root.wm_iconphoto(True, icon_image)
        

window_text = ttk.Label(mainframe, text="Server-Launcher")
window_text.grid(column=1, row=0, sticky=W)

#Define Functions
def back():
    root.destroy()
    subprocess.Popen(["pythonw", "GUIStart.pyw"])

def create_buttons():
    ttk.Button(mainframe, text="Back", command=back).grid(column=0, row=0, sticky=W)
    ttk.Button(mainframe, text="Start Server", command=lambda:accepting_eula (messagebox, server_launching)).grid(column=0, row=1, sticky=W)


#Create Buttons
create_buttons()

#Starting Mainloop
root.mainloop()

input("Press Enter to exit...")
