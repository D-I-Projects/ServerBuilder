import tkinter as tk
from tkinter import ttk, Scale, messagebox
import sys
import subprocess
import os
import logging
import datetime
from functions import get_config
from threading import Thread


def log_settings():
    log_dir = "ServerBuilder_Log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = os.path.join(log_dir, f"Server_Builder_GUILaunchServer - {current_datetime}.log")

    logger = logging.getLogger("ServerBuilder_GUILaunchServer")
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

logger.info("GUIProgramInformation.py was opened!")

RAM = int(get_config('Hardware', 'ram'))
Max_RAM = RAM * (3/4)

root = tk.Tk()
root.title("Launch Server")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
icon_image = tk.PhotoImage(file="sbicon.png")
root.wm_iconphoto(True, icon_image)

def window_text():
    window_text1 = ttk.Label(mainframe, text="Launch Server", font=("Open Sans", 16), underline=True)
    window_text1.grid(column=0, row=0, sticky=tk.W)

    window_text2 = ttk.Label(mainframe, text=f"You've got {RAM} GB RAM but you only can use {Max_RAM} GB")
    window_text2.grid(column=4, row=2, sticky=tk.W)

    window_text3 = ttk.Label(mainframe, text="Other", font=("Open Sans", 12))
    window_text3.grid(column=0, row=4, sticky=tk.W)

def create_slides():
    ram_scale = Scale(mainframe, from_=1, to=Max_RAM, orient=tk.HORIZONTAL)
    ram_scale.grid(column=0, row=1, columnspan=8, sticky=(tk.EW))
    return ram_scale

ram_scale = create_slides()

def value1():
    global ram_scale
    logger.info("Opening a dialog to accept the EULA.")
    messagebox12 = messagebox.askyesno("Server Builder", "By starting the server, you accept the Minecraft End User License Agreement.")
    if not messagebox12:  
        logger.info("User did not accept the EULA.")
        return
    
    file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "eula.txt")

    try:
        with open(file_path, 'w') as file:
            file.write("eula=true\n")
            logger.info(f"EULA-Datei erfolgreich erstellt: {file_path}")
    except FileNotFoundError:
            logger.error("Die Datei 'eula.txt' existiert nicht.")
    except PermissionError:
            logger.error("Keine Berechtigung zum Erstellen der Datei 'eula.txt'.")
    except Exception as e:
            logger.error(f"Fehler beim Erstellen der EULA-Datei: {e}")
    
    logger.info("Benutzer hat Minecrafts Eula akzeptiert.")
    ram_value = ram_scale.get()
    serverlaunching(ram_value)

def serverlaunching(ram_value):
    def launch():
        logger.info("User pressed Start Server...")
        os.system(f"java -Xmx{ram_value}G -jar Minecraft_jar_file/server.jar")

    server_thread = Thread(target=launch)
    server_thread.start()

def back():
    logger.info("User pressed back...")
    root.destroy()
    subprocess.Popen([sys.executable, "GUIStart.py"])
    

def create_buttons():
    ttk.Button(mainframe, text="Back", command=back).grid(column=0, row=5, sticky=tk.W)
    ttk.Button(mainframe, text="Start Server", command=value1).grid(column=0, row=2, sticky=tk.W)
    
window_text()
create_buttons()

root.mainloop()
