from tkinter import *
from tkinter import ttk
import os
import logging
import datetime
import tkinter as tk
from tkinter import filedialog
import shutil
import subprocess

current_dir = os.path.dirname(os.path.realpath(__file__))

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

root = Tk()
root.title("Plugins")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
icon_image = PhotoImage(file="sbicon.png")
root.wm_iconphoto(True, icon_image)

window_text = ttk.Label(mainframe, text="Plugins", font=("Open Sans", 16), underline=True)
window_text.grid(column=0, row=0, sticky=W)

window_text = ttk.Label(mainframe, text="Other", font=("Open Sans", 12), underline=True)
window_text.grid(column=0, row=3, sticky=W)

listbox = tk.Listbox(mainframe, bg="white", fg="blue", width=50, height=10)
listbox.grid(column=0, row=1, sticky=(tk.W, tk.E), padx=5, pady=5)

current_dir = os.path.dirname(os.path.realpath(__file__))
directory_path = os.path.join(current_dir, "plugins")

def show_folder_contents():
    listbox.delete(0, tk.END)
    for item in os.listdir(directory_path):
        listbox.insert(tk.END, item)
    root.after(1000, show_folder_contents)

show_folder_contents()

def add_plugin():
    file_path = filedialog.askopenfilename(filetypes=[("Jar files", "*.jar")])
    if file_path and os.path.isfile(file_path):
        # Zielordner für Plugins
        plugins_folder = "plugins"
        # Erstellen des Plugins-Ordners, falls er noch nicht existiert
        if not os.path.exists(plugins_folder):
            os.makedirs(plugins_folder)
        
        # Datei in den Plugins-Ordner kopieren
        try:
            shutil.copy(file_path, plugins_folder)
            print("Plugin erfolgreich hinzugefügt:", os.path.basename(file_path))
        except Exception as e:
            print("Fehler beim Hinzufügen des Plugins:", e)
    else:
        print("Keine gültige .jar-Datei ausgewählt.")
        
def back():
    logger.info("User pressed back...")
    root.destroy()
    subprocess.Popen(["python3", "GUIStart.py"])

def create_button():
    ttk.Button(mainframe, text="Add plugin", command=add_plugin).grid(column=0, row=2, sticky=W)
    ttk.Button(mainframe, text="Back", command=back).grid(column=0, row=4, sticky=W)

create_button()

root.mainloop()

input("Press Enter to exit...")
