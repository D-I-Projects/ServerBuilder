#Imports
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import Listbox
from tkinter import filedialog
from tkinter import DISABLED
from tkinter import NORMAL
from tkinter import BooleanVar
from Functions import no_feature, update_code, exit, do_you_like_to_continue_afterbuild, set_settings_setup_server, server_launching, no_selection
import sys
import os
import requests
import time
from tkinter.ttk import Style

#Mainframe
root = Tk()
root.title("Server Builder")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.geometry("250x120")
root.iconbitmap("icon.ico")

#Variables
server_providers = ["Vanilla 1.20.4", "PaperMC 1.20.4", "Spigot 1.20.4", "Purpur 1.20.4"]
mainframe = ttk.Frame(root, padding="3 3 12 12")
providervar = StringVar(value=server_providers)
provider_listbox = Listbox(mainframe, height=len(server_providers), listvariable=providervar)
Minecraft_Version_Downloads = [
    ["Vanilla 1.20.4" , "https://piston-data.mojang.com/v1/objects/8dd1a28015f51b1803213892b50b7b4fc76e594d/server.jar"],
    ["PaperMC 1.20.4" , "https://api.papermc.io/v2/projects/paper/versions/1.20.4/builds/485/downloads/paper-1.20.4-485.jar"],
    ["Spigot 1.20.4" , "https://download.getbukkit.org/spigot/spigot-1.20.4.jar"],
    ["Purpur 1.20.4" , "https://api.purpurmc.org/v2/purpur/1.20.4/latest/download"]
]

#Set Developer Mode
for Arg in sys.argv:
    print(Arg)
    if "-developer=true" == Arg:
        developer_mode = True
    else:
        developer_mode = False

#Define Functions
def back():
    root.destroy()
    os.system(f"python3 ./Start.py -developer={str(developer_mode).lower()}")


def create_buttons():
    ttk.Button(mainframe, text="Back", command=back).grid(column=0, row=1, sticky=W)
    ttk.Button(mainframe, text="Start Download", command=lambda:do_you_like_to_continue_afterbuild(messagebox, download_server_data)).grid(column=1, row=1, sticky=W)
    if developer_mode == True:
        ttk.Button(mainframe, text="Update Code", command=lambda:update_code(os, root, developer=developer_mode)).grid(column=2, row=1, sticky=W)

def display_content():
    for provider in server_providers:
        provider_listbox.insert("end", provider)

    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)


def download_server_data():
    fileneame = "server.jar"
    build_directory = filedialog.askdirectory()
    selected_indices = provider_listbox.curselection()
    if selected_indices:
        string = str(server_providers[selected_indices])
        for x in Minecraft_Version_Downloads:
            if Minecraft_Version_Downloads[x][0] == string:
                url = Minecraft_Version_Downloads[x][1]
                break
        response = requests.get(url)
        with open(f"{build_directory}/{filename}", "wb") as server_data:
            server_data.write(response.content)
      

#Set Settings
set_settings_setup_server(root, provider_listbox, mainframe, N, W, E, S)

#Create Buttons
create_buttons()

#Display Content
display_content()

#Starting Mainloop
root.mainloop()

input("Press Enter to exit...")


