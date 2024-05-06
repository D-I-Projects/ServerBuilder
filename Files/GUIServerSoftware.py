import tkinter as tk
from tkinter import ttk, messagebox
import requests
import os
import threading
import subprocess
import logging
import datetime
from tkinter import PhotoImage

def log_settings():
    log_dir = "ServerBuilder_Log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = os.path.join(log_dir, f"Server_Builder_GUIServerSoftware - {current_datetime}.log")

    logger = logging.getLogger("ServerBuilder_GUIServerSoftware")
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

logger = log_settings()

logger.info("GUIServerSoftware.py was opened!")

def start_download(tree):
    
    selected_item = tree.focus()
    if not selected_item:
        logger.info("No version selected!")
        messagebox.showerror("Error", "Please select a server version to download.")
        return
    
    values = tree.item(selected_item, "values")
    url = values[1]
    
    filename = "server.jar"
    build_directory = "Minecraft_jar_file"
    file_path = os.path.join(build_directory, filename)
    
    def update_progress(percent):
        progress_var.set(percent)
        
    def download_file():
        response = requests.get(url, stream=True)
        total_size = int(response.headers.get('content-length', 0))
        bytes_downloaded = 0
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
                    bytes_downloaded += len(chunk)
                    percent = (bytes_downloaded / total_size) * 100
                    root.after(100, update_progress, percent)
        
        messagebox.showinfo("Server Builder", "The server software has been downloaded successfully.")
    
    download_thread = threading.Thread(target=download_file)
    download_thread.start()


def back():
    logger.info("User pressed back...")
    root.destroy()
    subprocess.Popen(["python3", "GUIStart.py"])
        
root = tk.Tk()
root.title("Server Software")
icon_image = PhotoImage(file="sbicon.png")
root.wm_iconphoto(True, icon_image)
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

tree = ttk.Treeview(mainframe, columns=("Name", "Download Link", "Release Date"), show="headings", selectmode="browse")
tree.heading("Name", text="Name")
tree.heading("Download Link", text="Download Link")
tree.heading("Release Date", text="Release Date")
tree.column("Name", width=200)
tree.column("Download Link", width=340)
tree.column("Release Date", width=100)
tree.grid(row=1, column=0, columnspan=2, sticky="nsew")

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
for provider_data in Minecraft_Version_Downloads:
    tree.insert("", "end", values=provider_data)

progress_var = tk.DoubleVar()
progress_bar = ttk.Progressbar(mainframe, orient="horizontal", length=200, mode="determinate", variable=progress_var)
progress_bar.grid(row=2, column=0, columnspan=2, sticky="ew")

start_button = ttk.Button(mainframe, text="Start Download", command=lambda: start_download(tree))
start_button.grid(row=3, column=0, columnspan=2, sticky="ew")
back_button = ttk.Button(mainframe, text="Back", command=back)
back_button.grid(row=4, column=0, columnspan=2, sticky="ew")


root.mainloop()
