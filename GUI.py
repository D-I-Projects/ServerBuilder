#Imports
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import Listbox
from tkinter import filedialog
from tkinter import DISABLED
from tkinter import NORMAL
from tkinter import BooleanVar
from Functions import no_feature, update_code, exit, set_settings_setup_server
import sys
import os
import requests
import time

#Variables
root = Tk()
server_providers = ["Vanilla", "PaperMC"]
mainframe = ttk.Frame(root, padding="3 3 12 12")
providervar = StringVar(value=server_providers)
provider_listbox = Listbox(mainframe, height=len(server_providers), listvariable=providervar)
URLs = [["https://piston-data.mojang.com/v1/objects/8dd1a28015f51b1803213892b50b7b4fc76e594d/server.jar", True, "Vanilla-Minecraft(Latest-Version-Only)"], ["no link", False, ""]] #[Download Link, Only Latest Version]
LatesVersion_CheckButton = BooleanVar(value=True)
provider_listbox.selection_set(0)

#Set Developer Mode
for Arg in sys.argv:
    print(Arg)
    if "-developer=true" == Arg:
        developer_mode = True
    else:
        developer_mode = False

def download_server_data():
    listbox_index = provider_listbox.curselection()[0]
    build_directory = filedialog.askdirectory()
    response = requests.get(URLs[int(listbox_index)][0])
    with open("server.jar", "wb") as server_data:
        server_data.write(response.content)

#Define Functions
def do_you_like_to_continue():
    if messagebox.askyesno(title="Continue", message="Do You Want To Continue? In This Version You Can't Change Anything After Building!"):
        download_server_data()
def create_buttons():
    ttk.Button(mainframe, text="Exit", command=lambda:exit(sys, messagebox)).grid(column=0, row=1, sticky=W)
    ttk.Button(mainframe, text="Start", command=do_you_like_to_continue).grid(column=1, row=1, sticky=W)
    test = Checkbutton(root, text="Latest Version", variable=LatesVersion_CheckButton).grid(column=0, row=3, sticky=W)
    if developer_mode == True:
        ttk.Button(mainframe, text="Update Code", command=lambda:update_code(os, root, developer=developer_mode)).grid(column=2, row=1, sticky=W)

def display_content():
    for provider in server_providers:
        provider_listbox.insert("end", provider)

    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)








#Set Settings
set_settings_setup_server(root, provider_listbox, mainframe, N, W, E, S)

#Create Buttons
create_buttons()

#Display Content
display_content()

#Starting Mainloop
root.mainloop()


