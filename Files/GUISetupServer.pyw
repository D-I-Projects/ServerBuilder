#Imports
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import Listbox
from tkinter import filedialog
from tkinter import DISABLED
from tkinter import NORMAL
from tkinter import BooleanVar
from Functions import no_feature, exit, do_you_like_to_continue_afterbuild, set_settings_setup_server, server_launching, no_selection
import sys
import os
import requests
import pip._vendor.requests 
import time
from tkinter.ttk import Style
from tkinter import Tk, PhotoImage
import subprocess


#Mainframe
root = Tk()
root.title("Setup Server")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.geometry("250x120")
icon_image = PhotoImage(file="icon.png")
root.wm_iconphoto(True, icon_image)

#Variables
server_providers = ["Vanilla 1.20.4", "PaperMC 1.20.4", "Spigot 1.20.4", "Purpur 1.20.4"]
mainframe = ttk.Frame(root, padding="3 3 12 12")
providervar = StringVar(value=server_providers)
provider_listbox = Listbox(mainframe, height=len(server_providers), listvariable=providervar)
Minecraft_Version_Downloads = [
    ["Vanilla 1.20.4" , "https://mcversions.net/download/1.20.4"],
    ["PaperMC 1.20.4" , "https://api.papermc.io/v2/projects/paper/versions/1.20.4/builds/485/downloads/paper-1.20.4-485.jar"],
    ["Spigot 1.20.4" , "https://download.getbukkit.org/spigot/spigot-1.20.4.jar"],
    ["Purpur 1.20.4" , "https://api.purpurmc.org/v2/purpur/1.20.4/latest/download"]
]


window_text = ttk.Label(mainframe, text="Setup-Server")
window_text.grid(column=1, row=2, sticky=W)

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
    subprocess.Popen(["pythonw", "GUIStart.pyw"])


def create_buttons():
    ttk.Button(mainframe, text="Back", command=back).grid(column=0, row=1, sticky=W)
    ttk.Button(mainframe, text="Start Download", command=lambda: do_you_like_to_continue_afterbuild(messagebox, lambda: download_server_data(server_providers, Minecraft_Version_Downloads, provider_listbox))).grid(column=1, row=1, sticky=W)

def display_content():
    for provider in server_providers:
        provider_listbox.insert("end", provider)

    for child in mainframe.winfo_children(): 
        child.grid_configure(padx=5, pady=5)

#AI generiert, bevor weiteren Verknüpfungen bitte zusammenhang verstehen / Script verstehen
def download_server_data(server_providers, Minecraft_Version_Downloads, provider_listbox):
    filename = "server.jar"
    build_directory = "Minecraft_jar_file"
    selected_indices = provider_listbox.curselection()
    if selected_indices:
        selected_provider_index = selected_indices[0]
        selected_provider = server_providers[selected_provider_index]                               
        for version_data in Minecraft_Version_Downloads:
            if version_data[0] == selected_provider:
                url = version_data[1]
                response = requests.get(url)
                if response.status_code == 200:
                    with open(f"{build_directory}/{filename}", "wb") as server_data:
                        server_data.write(response.content)
                    print("Download successful.")
                else:
                    print(f"Failed to download. Status code: {response.status_code}")
                return
        print("No matching version found.")
    else:
        print("No provider selected.")
      

#Set Settings
set_settings_setup_server(root, provider_listbox, mainframe, N, W, E, S)

#Create Buttons
create_buttons()

#Display Content
display_content()

#Starting Mainloop
root.mainloop()

input("Press Enter to exit...")


