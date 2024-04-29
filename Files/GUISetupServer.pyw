#Imports
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
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
root.geometry("665x281")
icon_image = PhotoImage(file="icon.png")
root.wm_iconphoto(True, icon_image)

Minecraft_Version_Downloads = [
    ["Vanilla 1.20.5 (Works)" , "https://piston-data.mojang.com/v1/objects/79493072f65e17243fd36a699c9a96b4381feb91/server.jar", "2024-04-23"],
    ["PaperMC 1.20.5 (Experimental)" , "https://api.papermc.io/v2/projects/paper/versions/1.20.5/builds/22/downloads/paper-1.20.5-22.jar", "2024-4-24"],
    ["Vanilla 1.20.4 (Works)" , "https://piston-data.mojang.com/v1/objects/8dd1a28015f51b1803213892b50b7b4fc76e594d/server.jar", "2023-12-07"],
    ["PaperMC 1.20.4 (Works)" , "https://api.papermc.io/v2/projects/paper/versions/1.20.4/builds/485/downloads/paper-1.20.4-485.jar", "2024-04-29"],
    ["Spigot 1.20.4 (Works)" , "https://download.getbukkit.org/spigot/spigot-1.20.4.jar", "2024-01-08"],
    ["Purpur 1.20.4 (Works)" , "https://api.purpurmc.org/v2/purpur/1.20.4/2176/download", "2024-04-24"],
    ["Vanilla 1.20.3 (Works)" , "https://piston-data.mojang.com/v1/objects/4fb536bfd4a83d61cdbaf684b8d311e66e7d4c49/server.jar", "2023-12-04"],
    ["Vanilla 1.20.2 (Works)" , "https://piston-data.mojang.com/v1/objects/5b868151bd02b41319f54c8d4061b8cae84e665c/server.jar", "2023-09-20"],
    ["Spigot 1.20.2 (Works)" , "https://download.getbukkit.org/spigot/spigot-1.20.2.jar", "2023-12-05"],
]

#Treeview
tree = ttk.Treeview(mainframe, columns=("Name", "Download Link", "Release Date"), show="headings", selectmode="browse")
tree.heading("Name", text="Name")
tree.heading("Download Link", text="Download Link")
tree.heading("Release Date", text="Release Date")
tree.column("Name", width=200)
tree.column("Download Link", width=340)
tree.column("Release Date", width=100)
tree.grid(row=0, column=0, columnspan=2, sticky="nsew")
vsb = ttk.Scrollbar(mainframe, orient="vertical", command=tree.yview) #Funktion
vsb.grid(row=0, column=2, sticky='ns') #Scroll diagramm 
tree.configure(yscrollcommand=vsb.set) #Scrollcommand

#Insert data into Treeview
for provider_data in Minecraft_Version_Downloads:
    tree.insert("", "end", values=provider_data)

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
    ttk.Button(mainframe, text="Back", command=back).grid(column=0, row=2, sticky=W)
    ttk.Button(mainframe, text="Start Download", command=lambda: do_you_like_to_continue_afterbuild(messagebox, lambda: download_server_data(tree))).grid(column=0, row=1, sticky=W)

#AI generiert, bevor weiteren Verknüpfungen bitte zusammenhang verstehen / Script verstehen
def download_server_data(tree):
    selected_item = tree.focus()
    if selected_item:
        values = tree.item(selected_item, "values")
        url = values[1]
        response = requests.get(url)
        if response.status_code == 200:
            filename = "server.jar"
            build_directory = "Minecraft_jar_file"
            with open(f"{build_directory}/{filename}", "wb") as server_data:
                server_data.write(response.content)
            print("Download successful.")
        else:
            print(f"Failed to download. Status code: {response.status_code}")
    else:
        print("No provider selected.")

#Create Buttons
create_buttons()

#Starting Mainloop
root.mainloop()

input("Press Enter to exit...")