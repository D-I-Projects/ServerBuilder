from tkinter import *
from tkinter import ttk
import os
from tkinter import Tk, PhotoImage
import subprocess
import logging
import datetime

def log_settings():
    log_dir = "ServerBuilder_Log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = os.path.join(log_dir, f"Server_Builder_GUIProgramInformation - {current_datetime}.log")

    logger = logging.getLogger("ServerBuilder_GUIProgramInformation")
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

#Mainframe
root = Tk()
root.title("Program Information")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
icon_image = PhotoImage(file="sbicon.png")
root.wm_iconphoto(True, icon_image)

logger.info("File was opened!")

def back():
    logger.info("User pressed back...")
    root.destroy()
    subprocess.Popen(["python3", "GUISettings.py"])
    
    
def create_buttons():
    ttk.Button(mainframe, text="Back", command=back).grid(column=0, row=0, sticky=W)

def text_gui():
    window_text = ttk.Label(mainframe, text="Name : ServerBuilder")
    window_text.grid(column=0, row=1, sticky=W)
    window_text = ttk.Label(mainframe, text="Version : 1.7 (release)")
    window_text.grid(column=0, row=2, sticky=W)
    window_text = ttk.Label(mainframe, text="Release Date : 5.05.2024")
    window_text.grid(column=0, row=3, sticky=W)
    window_text = ttk.Label(mainframe, text="Autor's : wfxey, ivole32")
    window_text.grid(column=0, row=4, sticky=W)
    window_text = ttk.Label(mainframe, text="Release Plattform : GitHub")
    window_text.grid(column=0, row=5, sticky=W)

#Starting Mainloop
create_buttons()

text_gui()

root.mainloop()

input("Press Enter to exit...")
