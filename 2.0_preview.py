import os
import logging
import datetime
import shutil
import requests
import threading
import configparser
import platform
from tkinter import filedialog, messagebox
import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageTk
import pystray
from CTkListbox import *
import psutil
import sys
from pypresence import Presence
import time

#Discord Client ID
client_id = "1245459087584661513"

#Directory stuff
directory = "SB_FILES"
current_dir = os.getcwd()
path = os.path.join(current_dir, directory)

try:
    #Create SB_FILES
    os.mkdir(path)
    print("Verzeichnis '%s' erstellt" % directory)
except FileExistsError:
    print("Das Verzeichnis '%s' existiert bereits" % directory)
except PermissionError:
    print("Keine Berechtigung zum Erstellen des Verzeichnisses '%s'" % directory)
except Exception as e:
    print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")

#Logger Settings
def log_settings():
    log_dir = os.path.join(current_dir, "SB_FILES", "Logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = os.path.join(log_dir, f"ServerBuilder_v2.0_{current_datetime}.log")

    logger = logging.getLogger("ServerBuilder_v2.0")
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

#Icon download
def download_icon(icon_url, file_name):
    try:
        sb_files_dir = os.path.join(current_dir, 'SB_FILES')  # Pfad zum SB_FILES Verzeichnis
        if not os.path.exists(sb_files_dir):
            os.makedirs(sb_files_dir)  # Verzeichnis erstellen, wenn es nicht existiert

        file_path = os.path.join(sb_files_dir, file_name)  # Pfad zur Datei im SB_FILES Verzeichnis

        if os.path.exists(file_path):
            logger.info(f"The file {file_name} already exists.")
            return

        response = requests.get(icon_url)
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            logger.info(f"The icon file has been successfully downloaded and saved as {file_path}.")
        else:
            logger.error(f"Failed to download the icon file. Status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        logger.error(f"An error occurred while downloading the icon file: {e}")
    except OSError as e:
        logger.error(f"An error occurred while writing the icon file: {e}")

if __name__ == "__main__":
    icon_url = "https://raw.githubusercontent.com/wfxey/wfxey/main/icon.png"
    file_name = "icon.png"
    
    download_icon(icon_url, file_name)

#Config
class Config:
    def __init__(self):
        self.configparser = configparser
        self.platform = platform
        self.my_system = platform.uname()
        self.RAM = str(round(psutil.virtual_memory().total / (1024.**3)))

    def write_data(self):
        logger.info("Writing config.ini")
        config = self.configparser.ConfigParser()
        config['Hardware'] = {'RAM': self.RAM}
        config['System'] = {
            'System': self.my_system.system,
            'Release': self.my_system.release,
            'Version': self.my_system.version,
            'Machine': self.my_system.machine,
            'Processor': self.my_system.processor,
            'Python-Version': self.platform.python_version()
        }
        config['Advanced'] = {'Full-RAM': False, 'Developer': False}

        config_path = os.path.join(current_dir, 'SB_FILES', 'config.ini')
        with open(config_path, 'w') as configfile:
            config.write(configfile)

    def get_data(self, section, key):
        config = configparser.ConfigParser()
        config_path = os.path.join(current_dir, 'SB_FILES', 'config.ini')
        config.read(config_path)
        return config[section][key]

config = Config()
config.write_data()

#Stray
def load_image():
    image_path = os.path.join(current_dir, 'SB_FILES', 'icon.png')
    if os.path.exists(image_path):
        return Image.open(image_path)
    else:
        image = Image.new('RGB', (64, 64), (255, 255, 255))
        dc = ImageDraw.Draw(image)
        dc.rectangle((0, 0, 64, 64), fill=(0, 128, 255))
        dc.rectangle((16, 16, 48, 48), fill=(255, 255, 255))
        return image

def create_tray_icon():
    icon = pystray.Icon("test_icon")
    icon.icon = load_image()
    icon.title = "Server Builder v2.0"
    icon.run()

def start_tray_icon():
    tray_thread = threading.Thread(target=create_tray_icon, daemon=True)
    tray_thread.start()
    
#Get config
def get_config(section, key):
    logger.info("Loaded config.")
    config = configparser.ConfigParser()
    config_path = os.path.join(current_dir, 'SB_FILES', 'config.ini')
    config.read(config_path)
    if section in config and key in config[section]:
        return config[section][key]
    else:
        logger.error("Section '%s' or key '%s' not found in the configuration.", section, key)
        return None

#Check connection
def check_internet_connection():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        if response.status_code == 200:
            logger.info("Connection established!")
            return True
    except requests.RequestException:
        logger.info("No connection!")
        messagebox.showwarning("Warning", "No internet!")
        return False

#Switching between Pages
def switch(page):
    for fm in main_fm.winfo_children():
        fm.destroy()
    page()

#Some Variables
current_dir = os.path.dirname(os.path.realpath(__file__))
logger.info("Current Directory = %s", current_dir)

RAM = int(get_config('Hardware', 'ram'))
Max_RAM = RAM * (3/4)
logger.info("Max RAM = %f", Max_RAM)

plugins_folder_path = os.path.join(current_dir, "SB_FILES", "plugins")
logger.info("Plugins folder path = %s", plugins_folder_path)

if not os.path.exists(plugins_folder_path):
    os.makedirs(plugins_folder_path)
    logger.info("Plugins folder created at: %s", plugins_folder_path)

#Remove Plugin
def remove_plugin():
    initial_dir = os.path.join(current_dir, "SB_FILES", "plugins")
    file_path = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("Jar files", "*.jar")])
    if not file_path:  
        return
    try:
        os.remove(file_path)  
        logger.info("Plugin successfully removed: %s", os.path.basename(file_path))
    except Exception as e:
        logger.error("Error removing plugin: %s", e)

#Add Plugin
def add_plugin():  
    initial_dir = os.path.join(current_dir)
    file_path = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("Jar files", "*.jar")])
    if file_path and os.path.isfile(file_path):
        plugins_folder = os.path.join(initial_dir, "SB_FILES", "plugins")
        if not os.path.exists(plugins_folder):
            os.makedirs(plugins_folder)
        try:
            shutil.copy(file_path, plugins_folder)
            logger.info("Plugin successfully added: %s", os.path.basename(file_path))
        except Exception as e:
            logger.error("Error adding plugin: %s", e)
    else:
        logger.info("No valid .jar file selected.")

def icon_path():
    return os.path.join(os.getcwd(), 'SB_FILES', 'icon.png')

if check_internet_connection():
    app = ctk.CTk()
    app.geometry("900x500")
    app.title("Server Builder")
    app.wm_iconbitmap()
    icon = icon_path()
    app.iconphoto(False, ImageTk.PhotoImage(file=icon))
    app.resizable(width=False, height=False)
    
    if sys.platform == "win32":
        threading.Thread(target=create_tray_icon, daemon=True).start()
    else:
        logger.error("Das Tray-Icon wird nur auf Windows unterstützt.")
        
    #Sidebar / Navigation Bar
    sidebar_fm = tk.Frame(app, bg="black", width=200)
    sidebar_fm.pack(side=tk.LEFT, fill=tk.Y)

    server_builder_lbl = tk.Label(sidebar_fm, text="Server Builder", font=("Open Sans", 16), fg="white", bg="black")
    server_builder_lbl.pack(side=tk.TOP, pady=(15, 0), padx=10)

    options_fm = tk.Frame(sidebar_fm, bg="black")
    options_fm.pack(fill=tk.Y, padx=10, pady=10)

    home_btn = ctk.CTkButton(options_fm, text="Home", font=("Open Sans", 15), command=lambda: switch(home_page))
    home_btn.pack(fill=tk.X, pady=5)

    launcher_btn = ctk.CTkButton(options_fm, text="Launcher", font=("Open Sans", 15), command=lambda: switch(launcher_page))
    launcher_btn.pack(fill=tk.X, pady=5)

    software_btn = ctk.CTkButton(options_fm, text="Software", font=("Open Sans", 15), command=lambda: switch(software_page))
    software_btn.pack(fill=tk.X, pady=5)

    plugins_btn = ctk.CTkButton(options_fm, text="Plugins", font=("Open Sans", 15), command=lambda: switch(plugins_page))
    plugins_btn.pack(fill=tk.X, pady=5)
    
    settings_btn = ctk.CTkButton(options_fm, text="Settings", font=("Open Sans", 15), command=lambda: switch(settings_page))
    settings_btn.pack(fill=tk.X, pady=5)

    server_builder_lbl = tk.Label(sidebar_fm, text="Copyright (c) 2024 D&I Projects", font=("Open Sans", 6), fg="white", bg="black")
    server_builder_lbl.pack(side=tk.BOTTOM, pady=(0, 10), padx=10)

    main_fm = tk.Frame(app, bg="grey17")
    main_fm.pack(fill=tk.BOTH, expand=True)

#Home Page
def home_page():
    logger.info("Loaded Home Page")
    home_frame = ctk.CTkFrame(main_fm)
    home_frame.pack(fill=tk.BOTH, expand=True)
    tabview = ctk.CTkTabview(master=home_frame, width=700, height=450)
    tabview.pack(padx=40, pady=20)

    tabview.add("News")
    tabview.add("Changelog")
    tabview.add("About")
    tabview.set("News")
    
    #Elements for News
    label1 = ctk.CTkLabel(text="News", font=("Open Sans", 25), master=tabview.tab("News"))
    label1.pack(padx = 20, pady = 10)
    label = ctk.CTkLabel(text="Coming soon!", font=("Open Sans", 17), master=tabview.tab("News"))
    label.pack()
    
    #Elements for Changelog
    label = ctk.CTkLabel(text="Changelog", font=("Open Sans", 25), master=tabview.tab("Changelog"))
    label.pack(padx = 20, pady = 10)
    label = ctk.CTkLabel(text="- New design", font=("Open Sans", 13), master=tabview.tab("Changelog"))
    label.pack()
    label = ctk.CTkLabel(text="- Fixed the Launch Server function", font=("Open Sans", 13), master=tabview.tab("Changelog"))
    label.pack()
    label = ctk.CTkLabel(text="- Improved the installation file", font=("Open Sans", 13), master=tabview.tab("Changelog"))
    label.pack()
    
    #Elements for About
    label = ctk.CTkLabel(text="About", font=("Open Sans", 25), master=tabview.tab("About"))
    label.pack(padx = 20, pady = 10)
    
    label = ctk.CTkLabel(text="v2.0 GitHub", font=("Open Sans", 13), master=tabview.tab("About"))
    label.pack()
    label = ctk.CTkLabel(text="@wfxey @ivole32", font=("Open Sans", 13), master=tabview.tab("About"))
    label.pack()
    label = ctk.CTkLabel(text="Licenses are inside the license file and the THIRD_PARTY_LICENSES folder", font=("Open Sans", 13), master=tabview.tab("About"))
    label.pack()
    label = ctk.CTkLabel(text="Copyright (c) 2024 D&I Projects", font=("Open Sans", 13), master=tabview.tab("About"))
    label.pack()
    
    
#Plugins
def plugins_page():
    logger.info("Loaded Plugins Page")
    plugins_frame = ctk.CTkFrame(main_fm)
    plugins_frame.pack(fill=tk.BOTH, expand=True)
    
    global listbox
    listbox = CTkListbox(plugins_frame)
    listbox.pack(fill="both", expand=True, padx=10, pady=10)
    
    create_button1 = ctk.CTkButton(plugins_frame, text="Add plugin", command=add_plugin)
    create_button1.pack(pady=10)  
    
    create_button2 = ctk.CTkButton(plugins_frame, text="Remove plugin", command=remove_plugin)
    create_button2.pack(pady=10)  
    
    plugins_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    plugins_frame.pack(fill=tk.BOTH, expand=True)

    def show_folder_contents():
        global listbox
        listbox.delete(0, tk.END)
        for item in os.listdir(plugins_folder_path):
            listbox.insert(tk.END, item)
        app.after(1000, show_folder_contents)
        
    show_folder_contents()

def software_page():
    logger.info("Loaded Software Page")
    pass

def launcher_page():
    logger.info("Loaded Launcher Page")
    pass

def settings_page():
    logger.info("Loaded Settings Page")
    settings_frame = ctk.CTkFrame(main_fm)
    settings_frame.pack(fill=tk.BOTH, expand=True)
    
    settings_label = ctk.CTkLabel(settings_frame, text="Settings", font=("Open Sans", 25))
    settings_label.pack(pady=15)

def update_rich_presence():
    RPC = Presence(client_id)
    RPC.connect()
    while True:
        RPC.update(
            large_image="icon",
            details="Configuring Minecraft Server",
            state="Version 2.0",
            start=int(time.time())
        )
        time.sleep(60)

rpc_thread = threading.Thread(target=update_rich_presence)
rpc_thread.daemon = True
rpc_thread.start()

home_page()

app.mainloop()
