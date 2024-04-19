#Imports
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import Listbox
from tkinter import filedialog
from tkinter import DISABLED
from tkinter import NORMAL
from tkinter import BooleanVar
from Functions import no_feature, update_code, exit, do_you_like_to_continue_afterbuild, set_settings_setup_server, do_you_like_to_continue_only_if_installed_serverjar, server_launching
import sys
import os
import requests
import time
from tkinter.ttk import Style

# Hauptfenster erstellen
root = Tk()
root.title("Server Builder")

# Hauptframe erstellen
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.geometry("250x80")
#root.iconbitmap("icon.ico")
        
#Define Functions
def back():
    root.destroy()
    os.system(f"python3 ./Start.py")

def create_buttons():
    ttk.Button(mainframe, text="Back", command=back).grid(column=0, row=0, sticky=W)
    ttk.Button(mainframe, text="Start Server", command=lambda:do_you_like_to_continue_only_if_installed_serverjar(messagebox, server_launching)).grid(column=0, row=1, sticky=W)

def display_content():
    for child in mainframe.winfo_children():
        child.grid_configure(padx=5, pady=5)


#Create Buttons
create_buttons()

#Display Content
display_content()

#Starting Mainloop
root.mainloop()

input("Press Enter to exit...")
