#Imports
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import Listbox
import sys
import os

#Variables
root = Tk()
server_providers = ["Vanilla"]
mainframe = ttk.Frame(root, padding="3 3 12 12")
providervar = StringVar(value=server_providers)
provider_listbox = Listbox(mainframe, height=len(server_providers), listvariable=providervar)

#Set Developer Mode
for Arg in sys.argv:
    print(Arg)
    if "-developer=true" == Arg:
        developer_mode = True
    else:
        developer_mode = False

#Define Functions
def set_settings():
    root.title("MC Server Builder")
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)

    provider_listbox.grid(column=0, row=1)
    
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

def update_code():
    root.destroy()
    os.system("python3 ./GUI.py -developer=true")

def create_buttons():
    ttk.Button(mainframe, text="Exit", command=exit).grid(column=1, row=1, sticky=W)
    ttk.Button(mainframe, text="Start", command=do_you_like_to_continue).grid(column=2, row=1, sticky=W)
    if developer_mode == True:
        ttk.Button(mainframe, text="Update Code", command=update_code).grid(column=3, row=1, sticky=W)

def display_content():
    for provider in server_providers:
        provider_listbox.insert("end", provider)

    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)

def exit():
    if messagebox.askyesno(title="Exit?", message="Are You Shure That You Want To Exit?"):
        sys.exit(0)

def no_feature():
    messagebox.showinfo(title="No Feature", message="This Is An Feature That Isn't Implementet Yet!")
    if len(provider_listbox.curselection()) != 0 :
        print(int(provider_listbox.curselection()[-1]))

def do_you_like_to_continue():
    if messagebox.askyesno(title="Continue", message="Do You Want To Continue? In This Version You Can't Change Anything After Building!"):
        no_feature()

#Set Settings
set_settings()

#Create Buttons
create_buttons()

#Display Content
display_content()

#Start Mainloop
root.mainloop()
