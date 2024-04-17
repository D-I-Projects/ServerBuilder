#Imports
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import Listbox
from tkinter import filedialog
from tkinter import DISABLED
from tkinter import NORMAL
from tkinter import BooleanVar
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

#Set Developer Mode
for Arg in sys.argv:
    print(Arg)
    if "-developer=true" == Arg:
        developer_mode = True
    else:
        developer_mode = False

#Define Functions
def set_settings():
    root.title("MD Server Builder")

    provider_listbox.grid(column=0, row=2)
    provider_listbox.selection_set(0)
    
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

def update_code():
    root.destroy()
    os.system("python3 ./GUI.py -developer=true")

def create_buttons():
    ttk.Button(mainframe, text="Exit", command=exit).grid(column=0, row=1, sticky=W)
    ttk.Button(mainframe, text="Start", command=do_you_like_to_continue).grid(column=1, row=1, sticky=W)
    test = Checkbutton(root, text="Latest Version", state=DISABLED, variable=LatesVersion_CheckButton).grid(column=0, row=3, sticky=W)
    if URLs[int(provider_listbox.curselection()[-1])][1] == False:
        test = Checkbutton(root, text="Latest Version", variable=LatesVersion_CheckButton).grid(column=0, row=3, sticky=W)
    else:
        test = Checkbutton(root, text="Latest Version", state=DISABLED, variable=LatesVersion_CheckButton).grid(column=0, row=3, sticky=W)
    if developer_mode == True:
        ttk.Button(mainframe, text="Update Code", command=update_code).grid(column=2, row=1, sticky=W)

def display_content():
    for provider in server_providers:
        provider_listbox.insert("end", provider)

    if URLs[int(provider_listbox.curselection()[-1])][1] == False:
        test = Checkbutton(root, text="Latest Version", variable=LatesVersion_CheckButton).grid(column=0, row=3, sticky=W)

    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)

def exit():
    if messagebox.askyesno(title="Exit?", message="Are You Shure That You Want To Exit?"):
        sys.exit(0)

def no_feature():
    messagebox.showinfo(title="No Feature", message="This Is An Feature That Isn't Implementet Yet!")
    print(int(provider_listbox.curselection()[-1]))

def do_you_like_to_continue():
    if messagebox.askyesno(title="Continue", message="Do You Want To Continue? In This Version You Can't Change Anything After Building!"):
        build_directory = filedialog.askdirectory()
        response = requests.get(URLs[int(provider_listbox.curselection()[-1])][0])
        with open("server.jar", "w") as server_data:
            server_data.write(str(response.content))

def content_update():
    while 'normal' == root.state():
        for widget in mainframe.winfo_children():
            widget.destroy()
        create_buttons()
        time.wait(1)

#Set Settings
set_settings()

#Create Buttons
create_buttons()

#Display Content
display_content()

root.after(1, content_update)

#Starting Mainloop
root.mainloop()
