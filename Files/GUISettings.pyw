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
import webbrowser

#Mainframe
root = Tk()
root.title("Settings")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.geometry("250x115")
icon_image = PhotoImage(file="icon.png")
root.wm_iconphoto(True, icon_image)


window_text = ttk.Label(mainframe, text="Settings")
window_text.grid(column=2, row=0, sticky=W)

#Define Functions
def back():
    root.destroy()
    subprocess.Popen(["pythonw", "GUIStart.pyw"])
    
def program_information():
    root.destroy()
    subprocess.Popen(["pythonw", "GUIProgramInformation.pyw"])
    
def contact():
    root.destroy()
    subprocess.Popen(["pythonw", "GUIContact.pyw"])
    
def testedsystems():
        webbrowser.open_new_tab("TestedSystem.html")
  
def create_buttons():
    ttk.Button(mainframe, text="Back", command=back).grid(column=0, row=0, sticky=W)
    ttk.Button(mainframe, text="Informations", command=program_information).grid(column=0, row=2, sticky=W)
    ttk.Button(mainframe, text="Contacts", command=contact).grid(column=0, row=3, sticky=W)
    ttk.Button(mainframe, text="Tested Systems", command=testedsystems).grid(column=0, row=4, sticky=W)


#Create Buttons
create_buttons()

#Starting Mainloop
root.mainloop()

input("Press Enter to exit...")