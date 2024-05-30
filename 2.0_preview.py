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
import urllib.request
from threading import Thread

#Discord Client ID
client_id = "1245459087584661513"

#Directory stuff
directory = "SC_FILES"
current_dir = os.getcwd()
path = os.path.join(current_dir, directory)

try:
    #Create SC_FILES
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
    log_dir = os.path.join(current_dir, "SC_FILES", "Logs")
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

#Check connection
def check_internet_connection():
    try:
        response = requests.get("https://www.google.com", timeout=5)
        if response.status_code == 200:
            logger.info("Connection established!")
            return True
    except requests.RequestException:
        logger.critical("No connection! [CRITICAL], please solve this program before opening our program again!")
        messagebox.showwarning("StarCraft [CRITICAL]", "No internet! Cannot connect to (https://www.google.com). Server down? Please try again if you are connected to the internet! If it still doesnt work write us on our Discord Server or create a Issue on GitHub. We will solve it as fast as possible. Our program needs the Internet to sync our logo and other stuff. Please make sure that you have internet connection while using our Program! Maybe chedck if we released a new update on (https://github.com/Ivole32/Server-Builder)")
        return False
    
#Icon download
def download_icon(icon_url, file_name):
    try:
        SC_FILES_dir = os.path.join(current_dir, 'SC_FILES')  # Pfad zum SC_FILES Verzeichnis
        if not os.path.exists(SC_FILES_dir):
            os.makedirs(SC_FILES_dir)  # Verzeichnis erstellen, wenn es nicht existiert

        file_path = os.path.join(SC_FILES_dir, file_name)  # Pfad zur Datei im SC_FILES Verzeichnis

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

        config_path = os.path.join(current_dir, 'SC_FILES', 'config.ini')
        with open(config_path, 'w') as configfile:
            config.write(configfile)

    def get_data(self, section, key):
        config = configparser.ConfigParser()
        config_path = os.path.join(current_dir, 'SC_FILES', 'config.ini')
        config.read(config_path)
        return config[section][key]

config = Config()
config.write_data()

#Stray
def load_image():
    image_path = os.path.join(current_dir, 'SC_FILES', 'icon.png')
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
    icon.title = "StarCraft v2.0"
    icon.run()

def start_tray_icon():
    tray_thread = threading.Thread(target=create_tray_icon, daemon=True)
    tray_thread.start()
    
#Get config
def get_config(section, key):
    logger.info("Loaded config.")
    config = configparser.ConfigParser()
    config_path = os.path.join(current_dir, 'SC_FILES', 'config.ini')
    config.read(config_path)
    if section in config and key in config[section]:
        return config[section][key]
    else:
        logger.error("Section '%s' or key '%s' not found in the configuration.", section, key)
        return None

#Switching between Pages
def switch(page):
    for fm in main_fm.winfo_children():
        fm.destroy()
    page()

#Create CREATED_SERVERS.txt and override specific Line
def overwrite_specific_line(line_number, text):
    file_path = "SC_FILES/CREATED_SERVERS.txt"
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            pass
    
    with open(file_path, "r") as file:
        lines = file.readlines()

    if len(lines) >= line_number:
        if line_number != 1:
            lines[line_number - 1] = text + "\n"
        else:
            lines.insert(0, "\n")
            lines.insert(1, text + "\n")
    else:
        lines.extend(["\n"] * (line_number - len(lines) - 1))
        lines.append(text + "\n")

    with open(file_path, "w") as file:
        file.writelines(lines)

#__Check Lines__

def read_specific_value_from_config(config_index, section, key):
    config_path = os.path.join(current_dir, 'SC_FILES', f'Server_{config_index}.ini')
    config = configparser.ConfigParser()

    if os.path.exists(config_path):
        config.read(config_path)
        if section in config and key in config[section]:
            return config[section][key], True
        else:
            return None, False
    else:
        return None, False

# Line 1
cs_value1, success1 = read_specific_value_from_config(1, 'Server', 'Server Name')
logger.debug("Line 1 = %s Success = %s", cs_value1, success1)
if success1:
    logger.debug("Line 1 wurde erfolgreich gelesen.")
else:
    logger.debug("Fehler beim Lesen von Line 1.")

# Line 2
cs_value2, success2 = read_specific_value_from_config(2, 'Server', 'Server Name')
logger.debug("Line 2 = %s Success = %s", cs_value2, success2)
if success2:
    logger.debug("Line 2 wurde erfolgreich gelesen.")
else:
    logger.debug("Fehler beim Lesen von Line 2.")

# Line 3
cs_value3, success3 = read_specific_value_from_config(3, 'Server', 'Server Name')
logger.debug("Line 3 = %s Success = %s", cs_value3, success3)
if success3:
    logger.debug("Line 3 wurde erfolgreich gelesen.")
else:
    logger.debug("Fehler beim Lesen von Line 3.")

# Line 4
cs_value4, success4 = read_specific_value_from_config(4, 'Server', 'Server Name')
logger.debug("Line 4 = %s Success = %s", cs_value4, success4)
if success4:
    logger.debug("Line 4 wurde erfolgreich gelesen.")
else:
    logger.debug("Fehler beim Lesen von Line 4.")

# Line 5
cs_value5, success5 = read_specific_value_from_config(5, 'Server', 'Server Name')
logger.debug("Line 5 = %s Success = %s", cs_value5, success5)
if success5:
    logger.debug("Line 5 wurde erfolgreich gelesen.")
else:
    logger.debug("Fehler beim Lesen von Line 5.")




#Some Variables
current_dir = os.path.dirname(os.path.realpath(__file__))
logger.info("Current Directory = %s", current_dir)

OS = get_config('System', 'system')
OS_RELEASE = get_config('System', 'release')
RAM = float(get_config('Hardware', 'ram'))
PYTHON_VERSION = get_config("System", "python-version")
Max_RAM = RAM * (3/4)

logger.info("---------------------------------")
logger.info("Max RAM = %.2f", Max_RAM)
logger.info("OS = %s", OS)
logger.info("OS Release = %s", OS_RELEASE)
logger.info("Python Version = %s", PYTHON_VERSION)
logger.info("---------------------------------")

plugins_folder_path = os.path.join(current_dir, "SC_FILES", "plugins")
logger.info("Plugins folder path = %s", plugins_folder_path)

if not os.path.exists(plugins_folder_path):
    os.makedirs(plugins_folder_path)
    logger.info("Plugins folder created at: %s", plugins_folder_path)

#Remove Plugin
def remove_plugin():
    initial_dir = os.path.join(current_dir, "SC_FILES", "plugins")
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
        plugins_folder = os.path.join(initial_dir, "SC_FILES", "plugins")
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
    return os.path.join(os.getcwd(), 'SC_FILES', 'icon.png')

if check_internet_connection():
    app = ctk.CTk()
    app.geometry("1100x600")
    app.title("StarCraft")
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

    server_builder_lbl = tk.Label(sidebar_fm, text="StarCraft", font=("Open Sans", 16), fg="white", bg="black")
    server_builder_lbl.pack(side=tk.TOP, pady=(15, 0), padx=10)

    options_fm = tk.Frame(sidebar_fm, bg="black")
    options_fm.pack(fill=tk.Y, padx=10, pady=10)

    home_btn = ctk.CTkButton(options_fm, text="Home", font=("Open Sans", 15), command=lambda: switch(home_page))
    home_btn.pack(fill=tk.X, pady=5)

    software_btn = ctk.CTkButton(options_fm, text="Server", font=("Open Sans", 15), command=lambda: switch(server_page))
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
    tabview = ctk.CTkTabview(master=home_frame, width=900, height=550)
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
    label = ctk.CTkLabel(text="- Improved/New the installation file", font=("Open Sans", 13), master=tabview.tab("Changelog"))
    label.pack()
    label = ctk.CTkLabel(text="- Linux App Image", font=("Open Sans", 13), master=tabview.tab("Changelog"))
    label.pack()
    label = ctk.CTkLabel(text="- Server Page with Create Server function and more", font=("Open Sans", 13), master=tabview.tab("Changelog"))
    label.pack()
    label = ctk.CTkLabel(text="- Discord rich presence", font=("Open Sans", 13), master=tabview.tab("Changelog"))
    label.pack()
    label = ctk.CTkLabel(text="- System stray", font=("Open Sans", 13), master=tabview.tab("Changelog"))
    label.pack()
    label = ctk.CTkLabel(text="- New logo", font=("Open Sans", 13), master=tabview.tab("Changelog"))
    label.pack()
    
    #Elements for About
    label = ctk.CTkLabel(text="About", font=("Open Sans", 25), master=tabview.tab("About"))
    label.pack(padx = 20, pady = 10)
    
    label = ctk.CTkLabel(text="StarCraft v2.0 GitHub", font=("Open Sans", 13), master=tabview.tab("About"))
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

#Server Page
def server_page():
    logger.info("Loaded Software Page")
    server_frame = ctk.CTkFrame(main_fm)
    server_frame.pack(fill=tk.BOTH, expand=True)
    
    def radiobutton_event():
        logger.info("Current radiobutton value: %s", radio_var.get())
    
    server_label = ctk.CTkLabel(server_frame, text="New Server", font=("Open Sans", 25))
    server_label.pack(pady=15)
    
    create_server_page_btn = ctk.CTkButton(server_frame, text="Create Server", font=("Open Sans", 15), command=lambda: switch(create_server_page))
    create_server_page_btn.pack(padx=20, pady=15)
    
    server_label = ctk.CTkLabel(server_frame, text="Your Servers", font=("Open Sans", 25))
    server_label.pack(pady=15)
    
    global radio_var
    radio_var = ctk.IntVar(value=0)
    
    server_buttons = []

    # Iterate over available servers
    for i in range(1, 6):
        server_config, success = read_specific_value_from_config(i, 'Server', 'Server Name')
        
        if success:
            server_name = server_config
            radiobutton = ctk.CTkRadioButton(server_frame, text=server_name, command=radiobutton_event, variable=radio_var, value=i)
            radiobutton.pack(padx=10, pady=10)
            server_buttons.append(radiobutton)
        else:
            logger.info(f"Server {i} doesn't exist. (This is a common error!)")
    
    if server_buttons:
        confirm_button = ctk.CTkButton(server_frame, text="Confirm", command=perform_selected_action)
        confirm_button.pack(padx=10, pady=10)
    else:
        label = ctk.CTkLabel(server_frame, text="No Servers available!")
        label.pack(pady=10, padx=10)
            
            
def perform_selected_action():
    selected_option = radio_var.get()
    if selected_option == 1:
        logger.info("Selected (My Server 1)")
    elif selected_option == 2:
        logger.info("Selected (My Server 2)")
    elif selected_option == 3:
        logger.info("Selected (My Server 3)")
    elif selected_option == 4:
        logger.info("Selected (My Server 4)")
    elif selected_option == 5:
        logger.info("Selected (My Server 5)")

class DownloadGUI:
    def __init__(self, url, save_path):
        self.url = url
        self.save_path = save_path
        self.root = tk.Tk()
        self.root.title("Downloading")
        self.progress = ctk.CTkProgressBar(self.root, mode="indeterminate")
        self.progress.pack(padx=20, pady=10)
        
    def start_download(self):
        self.progress.start()
        self.root.after(100, self.download_file)
        self.root.mainloop()
        
    def download_file(self):
        urllib.request.urlretrieve(self.url, self.save_path)
        self.progress.stop()
        messagebox.showinfo("Download Completed", "The JAR file has been successfully downloaded and saved.")
        self.root.destroy()
        
#Create Server Page
class Config_Server:
    def __init__(self, server_name, version, software, max_players, filename='config_server.ini'):
        self.configparser = configparser
        self.server_name = server_name
        self.version = version
        self.software = software
        self.max_players = max_players
        self.filename = filename

    def write_data(self):
        logger.info(f"Writing {self.filename}")
        config = self.configparser.ConfigParser()
        config["Server"] = {
            'Server Name': self.server_name,
            'Selected Version': self.version,
            'Selected Software': self.software,
            'Max Player': self.max_players,
        }
        SC_FILES_dir = os.path.join(current_dir, 'SC_FILES')
        os.makedirs(SC_FILES_dir, exist_ok=True)

        # Find the next available server slot
        for i in range(1, 6):
            config_path = os.path.join(SC_FILES_dir, f'Server_{i}.ini')
            if not os.path.exists(config_path):
                with open(config_path, 'w') as configfile:
                    config.write(configfile)
                logger.info(f"Configuration saved to {config_path}")

                # Create server directory and download JAR file
                server_dir = os.path.join(SC_FILES_dir, f'Server_{i}')
                os.makedirs(server_dir, exist_ok=True)
                jar_url = get_jar_url(self.version, self.software)
                if jar_url:
                    jar_path = os.path.join(server_dir, 'server.jar')
                    urllib.request.urlretrieve(jar_url, jar_path)
                    logger.info(f"Server JAR downloaded to {jar_path}")
                else:
                    logger.warning("No URL found for JAR file.")
                
                return True 
        else:
            logger.warning("Server limit reached. Cannot create more servers.")
            return False

    def get_data(self, section, key):
        config = configparser.ConfigParser()
        config_path = os.path.join(current_dir, 'SC_FILES', self.filename)
        config.read(config_path)
        return config[section][key]

def get_jar_url(version, software):
    # Dictionary mit den URLs für verschiedene Versionen und Software
    jar_urls = {
        "1.20.6": {
            "Bukkit": "https://download.getbukkit.org/craftbukkit/craftbukkit-1.20.6.jar",
            "Spigot": "https://download.getbukkit.org/spigot/spigot-1.20.6.jar",
            "Vanilla": "https://piston-data.mojang.com/v1/objects/145ff0858209bcfc164859ba735d4199aafa1eea/server.jar"
        },
        "1.20.4": {
            "Bukkit": "https://download.getbukkit.org/craftbukkit/craftbukkit-1.20.4.jar",
            "Spigot": "https://download.getbukkit.org/spigot/spigot-1.20.4.jar",
            "Vanilla": "https://download.getbukkit.org/spigot/spigot-1.20.4.jar"
        },
        "1.19.4": {
            
        }
    }

    # Überprüfen, ob die Version und Software in den URLs vorhanden sind
    if version in jar_urls and software in jar_urls[version]:
        return jar_urls[version][software]
    else:
        # Wenn keine entsprechende URL gefunden wurde, gib None zurück
        return None

def create_server_page():
    logger.info("Loaded Create Server Page")
    create_server_frame = ctk.CTkFrame(main_fm)
    create_server_frame.pack(fill=tk.BOTH, expand=True)

    def confirm_create_server():
        server_name = entry.get()
        selected_version = selected_option.get()
        selected_software = software_option.get()
        player_count = int(round(player_slider.get()))
        logger.info(f"Server Name: {server_name}")
        logger.info(f"Selected Version: {selected_version}")
        logger.info(f"Selected Software: {selected_software}")
        logger.info(f"Max Player: {player_count}")

        config_server = Config_Server(server_name, selected_version, selected_software, player_count)
        success = config_server.write_data()
        
        if not success:
            messagebox.showwarning("Limit reached", "You can only own 5 servers at the same time!")

    def validate_inputs():
        if entry.get() and selected_option.get() != "Select Version" and software_option.get() != "Select Software":
            confirm_button.configure(state=tk.NORMAL, fg_color="green")
        else:
            confirm_button.configure(state=tk.DISABLED, fg_color="grey")

    def option_changed(choice):
        software_option.set("Select Software")
        software_menu.configure(values=[])

        if choice != "Select Version":
            software_menu.configure(state=tk.NORMAL, fg_color="grey7")
            software_menu.configure(values=["Bukkit", "Spigot", "Vanilla"])
        else:
            software_menu.configure(state=tk.DISABLED, fg_color="grey")

        validate_inputs()

    def open_progress_window(url, save_path):
        progress_window = tk.Toplevel()
        progress_window.title("Downloading JAR File")
        progress_window.geometry("300x100")

        progress_label = ctk.CTkLabel(progress_window, text="Downloading JAR File...")
        progress_label.pack(pady=10)

        progress_bar = ctk.CTkProgressBar(progress_window, length=200, mode='determinate')
        progress_bar.pack(pady=5)

        download_thread = Thread(target=download_jar_file, args=(url, save_path, progress_bar, progress_window))
        download_thread.start()

    def download_jar_file(url, save_path, progress_bar, progress_window):
        try:
            response = requests.get(url, stream=True)
            total_size = int(response.headers.get('content-length', 0))

            with open(save_path, 'wb') as file:
                bytes_downloaded = 0
                for data in response.iter_content(chunk_size=1024):
                    file.write(data)
                    bytes_downloaded += len(data)
                    progress_bar['value'] = (bytes_downloaded / total_size) * 100
                    progress_window.update_idletasks()

            messagebox.showinfo("Download Complete", "JAR file downloaded successfully!")
        except Exception as e:
            messagebox.showerror("Download Failed", f"Failed to download JAR file: {str(e)}")
        finally:
            progress_window.destroy()

    settings_label = ctk.CTkLabel(create_server_frame, text="Create Server", font=("Open Sans", 25))
    settings_label.pack(pady=15)
    
    name_label = ctk.CTkLabel(create_server_frame, text="Server Name", font=("Open Sans", 13))
    name_label.pack()
    
    entry = ctk.CTkEntry(create_server_frame, width=180, height=30, border_width=1, corner_radius=10, fg_color="grey7", placeholder_text="Server Name")
    entry.pack(pady=10, padx=10)
    entry.bind("<KeyRelease>", lambda event: validate_inputs())

    software_label = ctk.CTkLabel(create_server_frame, text="Server Version", font=("Open Sans", 13))
    software_label.pack(pady=(20, 0))

    selected_option = ctk.StringVar(value="Select Version")
    option_menu = ctk.CTkOptionMenu(create_server_frame, values=["1.20.6", "1.20.4", "1.20.2", "1.19.4", "1.18.2", "1.16.5", "1.12.2"], variable=selected_option, command=option_changed)
    option_menu.pack(pady=20)

    software_label = ctk.CTkLabel(create_server_frame, text="Server Software", font=("Open Sans", 13))
    software_label.pack(pady=(20, 0))

    software_option = ctk.StringVar(value="Select Software")
    software_menu = ctk.CTkOptionMenu(create_server_frame, values=[], variable=software_option, command=lambda choice: validate_inputs())
    software_menu.pack(pady=10)
    software_menu.configure(state=tk.DISABLED, fg_color="grey")

    player_count_label = ctk.CTkLabel(create_server_frame, text="Max Player", font=("Open Sans", 13))
    player_count_label.pack(pady=(20, 0))

    player_slider_frame = ctk.CTkFrame(create_server_frame)
    player_slider_frame.pack(pady=20)

    def update_slider_label(value):
        rounded_value = int(round(float(value)))
        slider_label.configure(text=f"Max Player: {rounded_value}")
    player_slider = ctk.CTkSlider(player_slider_frame, from_=2, to=100, command=update_slider_label)
    player_slider.pack()

    slider_label = ctk.CTkLabel(player_slider_frame, text="Player Count: 20", font=("Open Sans", 13))
    slider_label.pack(pady=10)

    confirm_button = ctk.CTkButton(create_server_frame, text="Confirm", font=("Open Sans", 16), command=confirm_create_server, state=tk.DISABLED, fg_color="grey")
    confirm_button.pack(side=ctk.BOTTOM, pady=(0, 10), padx=10)

    validate_inputs()  # Initial validation

def get_jar_url(version, software):
    # Dictionary mit den URLs für verschiedene Versionen und Software
    jar_urls = {
        "1.20.6": {
            "Bukkit": "https://example.com/bukkit-1.20.6.jar",
            "Spigot": "https://example.com/spigot-1.20.6.jar",
            "Vanilla": "https://piston-data.mojang.com/v1/objects/145ff0858209bcfc164859ba735d4199aafa1eea/server.jar"
        },
        "1.20.4": {
            "Bukkit": "https://example.com/bukkit-1.20.4.jar",
            "Spigot": "https://example.com/spigot-1.20.4.jar",
            "Vanilla": "https://example.com/vanilla-1.20.4.jar"
        },
        # Weitere Versionen und URLs hier hinzufügen
    }

    # Überprüfen, ob die Version und Software in den URLs vorhanden sind
    if version in jar_urls and software in jar_urls[version]:
        return jar_urls[version][software]
    else:
        # Wenn keine entsprechende URL gefunden wurde, gib None zurück
        pass

def dashboard():
    pass

def settings_page():
    logger.info("Loaded Settings Page")
    settings_frame = ctk.CTkFrame(main_fm)
    settings_frame.pack(fill=tk.BOTH, expand=True)
    
    settings_label = ctk.CTkLabel(settings_frame, text="Experimental", font=("Open Sans", 25))
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
