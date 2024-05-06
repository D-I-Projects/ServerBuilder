from tkinter import *
from tkinter import ttk
import os
import sys
import tkinter as tk
from tkinter import ttk
from functions import log_settings
import subprocess
from Launch import config
import logging
import datetime
import webbrowser
import requests
from tkinter import messagebox

current_dir = os.path.dirname(os.path.realpath(__file__))
html_file_path = os.path.join(current_dir, "Home.html")

config = config()
config.write_data()
def log_settings():
    log_dir = "ServerBuilder_Log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = os.path.join(log_dir, f"Server_Builder_GUIPStart - {current_datetime}.log")

    logger = logging.getLogger("ServerBuilder_GUIPStart")
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

logger.info("GUIStart.py was opened!")

#Mainframe
root = Tk()
root.title("Server Builder")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
icon_image = PhotoImage(file="sbicon.png")
root.wm_iconphoto(True, icon_image)
style = ttk.Style()
menubar = Menu(root)
root.config(menu=menubar)


url = "https://github.com/Ivole32/Server-Builder/releases/tag/v1.8-Windows"

def search_for_update():
    try:
        response = requests.get(url)
        if response.status_code == 200:
            logger.info("Die Verbindung zur Website wurde erfolgreich hergestellt.")
            answer = messagebox.askyesno("Server Builder", "A new update is available, do you want to download it?")
            if not answer:
                return
            webbrowser.open_new_tab("https://github.com/Ivole32/Server-Builder/releases")
        else:
            logger.error("Fehler: Die Website konnte nicht erreicht werden. Statuscode:", response.status_code)
            messagebox.showinfo("Server Builder", "There's no update available!")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Server Builder", "No connection to server!")
        logger.error("Fehler: Es konnte keine Verbindung zur Website hergestellt werden.", e)


themeMenu = Menu(menubar, tearoff=0, font=("Open Sans", 8))
menubar.add_cascade(label="Update", menu=themeMenu)
themeMenu.add_command(label="Search for update", command=search_for_update)

for Arg in sys.argv:
    print(Arg)
    if "-developer=true" == Arg:
        developer_mode = True
    else:
        developer_mode = False
    
window_text = ttk.Label(mainframe, text="Server Builder 1.7", font=("Open Sans", 16), underline=True)
window_text.grid(column=0, row=0, sticky=tk.W)

window_text = ttk.Label(mainframe, text="Other", font=("Open Sans", 12), underline=True)
window_text.grid(column=0, row=2, sticky=tk.W)

def setup_server():
    logger.info("User pressed Server Software...")
    root.destroy()
    subprocess.Popen(["python3", "GUIServerSoftware.py"])
    

def launch_server():
    logger.info("User pressed Launch Server...")
    root.destroy()
    subprocess.Popen(["python3", "GUILaunchServer.py"])
    
    
def settings():
    logger.info("User pressed Settings...")
    root.destroy()
    subprocess.Popen(["python3", "GUISettings.py"])

def plugins():
    logger.info("User pressed Plugins...")
    root.destroy()
    subprocess.Popen(["python3", "GUIPlugins.py"])
    
def get_config(section, key):
    config.get_data(section, key)
    
def open_website():
    logger.info("User pressed Website...")
    webbrowser.open_new_tab(html_file_path)
    
def create_button():
    ttk.Button(mainframe, text="Website", command=open_website).grid(column=1, row=4, sticky=(W,E), padx=5, pady=5)
    ttk.Button(mainframe, text="Launch Server", command=launch_server).grid(column=0, row=1, sticky=(W,E), padx=5, pady=5)
    ttk.Button(mainframe, text="Software", command=setup_server).grid(column=1, row=1, sticky=(W,E), padx=5, pady=5)
    ttk.Button(mainframe, text="Plugins", command=plugins).grid(column=2, row=1, sticky=(W,E), padx=5, pady=5)
    ttk.Button(mainframe, text="Settings", command=settings).grid(column=0, row=4, sticky=(W,E), padx=5, pady=5)


create_button()

root.mainloop()

input("Press Enter to exit...")

