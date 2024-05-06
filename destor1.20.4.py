import os
import logging
import datetime
import requests
from tkinter import *
from tkinter import ttk

def log_settings():
    log_dir = "Log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = os.path.join(log_dir, f"Destor - {current_datetime}.log")

    logger = logging.getLogger("Destor")
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

def download_icon(icon_url, file_name):
    try:
        if os.path.exists(file_name):
            logger.info(f"The file {file_name} already exists.")
            return
        
        response = requests.get(icon_url)
        if response.status_code == 200:
            with open(file_name, 'wb') as file:
                file.write(response.content)
            logger.info(f"The icon file has been successfully downloaded and saved as {file_name}.")
        else:
            logger.error(f"Failed to download the icon file. Status code: {response.status_code}")
    except Exception as e:
        logger.error(f"An error occurred while downloading the icon file: {e}")

if __name__ == "__main__":
    iconurl = "https://raw.githubusercontent.com/wfxey/Destor/main/icon.png"
    file_name = "icon.png"
    
    download_icon(iconurl, file_name)

root = Tk()
root.title("Destor 1.20.4")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.geometry("700x400")
icon_image = PhotoImage(file="icon.png")
root.wm_iconphoto(True, icon_image)
root.resizable(False, False)

def check_and_create_file(filename, content, logger):
    if not os.path.exists(filename):
        with open(filename, 'w') as f:
            f.write(content)
        logger.info(f"{filename} has been created with the default content.")
    else:
        logger.info(f"{filename} already exists.")

def check_and_create_folder(dirname, logger):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
        logger.info(f"{dirname} has been created.")
    else:
        logger.info(f"{dirname} already exists.")

#Files to check
check_and_create_file("server.properties", "server.properties", logger)
check_and_create_file("permissions.txt", "permissions.txt", logger)
check_and_create_file("ops.txt", "ops.txt", logger)
check_and_create_file("whitelist.txt", "whitelist.txt", logger)
check_and_create_file("eula.txt", "eula = false #Please read https://www.minecraft.net/en-us/eula", logger)
check_and_create_folder("world", logger)
check_and_create_folder("world_nether", logger)
check_and_create_folder("world_end", logger)

def text_gui():
    text1 = ttk.Label(mainframe, text="Destor 1.20.4", font=("Open Sans", 16), underline=True)
    text1.grid(column=0, row=0, sticky=W)

#def buttons_gui():
    #button1 = ttk.Button(mainframe, text="Start Server")
    #button1.grid(row=2, column=0, columnspan=2, sticky="ew")

#buttons_gui()
text_gui()
root.mainloop()
