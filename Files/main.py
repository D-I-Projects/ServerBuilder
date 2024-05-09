import tkinter as tk
from tkinter import *
import logging
import os
import requests
import datetime
import configparser
import psutil
import platform
import webbrowser
from tkinter import messagebox
import shutil
from tkinter import filedialog
import threading
import tkinter.ttk as ttk
import psutil
import sys


def check_internet_connection():
    try:
        response = requests.get("http://www.google.com", timeout=5)
        if response.status_code == 200:
            return True
    except requests.RequestException:
        # Show a message box indicating no internet connection
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showwarning("Warning", "No internet!")
    return False

check_internet_connection()

dir_plugins = "plugins"
if not os.path.exists(dir_plugins):
    os.makedirs(dir_plugins)
    
dir_server_jar = "Minecraft_jar_file"
if not os.path.exists(dir_server_jar):
    os.makedirs(dir_server_jar)


current_dir = os.path.dirname(os.path.realpath(__file__))

directory_path = os.path.join(current_dir, "plugins")

class config:
    def __init__(self):

        self.configparser = configparser
        self.platform = platform

        self.my_system = platform.uname()

        self.RAM = str(round(psutil.virtual_memory().total / (1024.**3)))

    def write_data(self):

        config = self.configparser.ConfigParser()
        config['Hardware'] = {'RAM': self.RAM}

        config['System'] = {'System': self.my_system.system, 'Release': self.my_system.release, 'Version': self.my_system.version, 'Machine': self.my_system.machine, 'Processor': self.my_system.processor, 'Python-Version': self.platform.python_version()}

        config['Advanced'] = {'Full-RAM': False, 'Developer': False}

        with open("config.ini", 'w') as configfile:
            config.write(configfile)

    def get_data(self, section, key):
        return config[section][key]
    
config = config()
config.write_data()

def log_settings():
    log_dir = "Log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = os.path.join(log_dir, f"ServerBuilder - {current_datetime}.log")

    logger = logging.getLogger("ServerBuilder")
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

def get_config(section, key):
    logger.info("Loaded get_config.")
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config[section][key]

def exit(sys, messagebox, title="Exit?", message="Are you sure that you want to exit?"):
    if messagebox.askyesno(title=title, message=message):
        sys.exit(0)
        logger.info("Loaded exit.")

def do_you_like_to_continue_afterbuild(messagebox, download_function):
    result = messagebox.askquestion("Continue", "Do you want to start the download?", icon='warning') 
    if result == 'yes':
        download_function()
    else:
        messagebox.showinfo("Cancelled", "Download cancelled.")
        logger.info("Loaded do_you_like_to_continue_afterbuild.")

def set_settings_setup_server(root, provider_listbox, mainframe, N, W, E, S):
    provider_listbox.grid(column=0, row=2)
    provider_listbox.selection_set(0)
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    logger.info("Loaded set_settings_setup_server.")

def do_you_like_to_continue_only_if_installed_serverjar(messagebox, function, title="Continue", message="Do you want to continue? If you didn't executed Setup-Server before, nothing will happen! Please also make sure you DO NOT have two different jar files in your folder!"):
    if messagebox.askyesno(title=title, message=message):
        function()
        logger.info("Loaded do_you_like_to_continue_only_if_installed_serverjar")
        
def accepting_eula(messagebox, function, title="Accepting eula!", message="With pressing yes your accepting the eula of Minecraft. The accepted eula is located inside eula.txt.", icon="warning"):
    if messagebox.askyesno(title=title, message=message):
        function()
        logger.info("Loaded accepting_eula.")

def no_selection(messagebox, title="No Selection", message="No selection for server Systems!"):
    messagebox.showinfo(title=title, message=message)
    logger.info("Loaded no_selection.")

RAM = int(get_config('Hardware', 'ram'))
Max_RAM = RAM * (3/4)

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
    iconurl = "https://github.com/Ivole32/Server-Builder/releases/download/v1.7/sbicon.png"
    file_name = "icon.png"
    
    download_icon(iconurl, file_name)
    

url = "https://github.com/Ivole32/Server-Builder/releases/tag/v1.9"

root = tk.Tk()
root.geometry("800x400")
root.title("Server Builder")
root.cget("bg")
icon_image = PhotoImage(file="icon.png")
root.wm_iconphoto(True, icon_image)
menubar = Menu(root)
root.config(menu=menubar)
root.resizable(width=False,height=False)

def delete_server_files1():
    logger.info("User pressed delete server files!")
    confirmation = messagebox.askyesno("Server Builder", "Are you sure that you want to continue? Your about to delete everything!")
    if not confirmation:
        logger.info("User cancelled!")
        return
    logger.info("User confirmed!")
    current_dir = os.path.dirname(os.path.realpath(__file__))
    plugins = os.path.join(current_dir, 'plugins')
    
    # Lösche das Plugin-Verzeichnis und seinen Inhalt
    shutil.rmtree(plugins)
    
    files_to_delete = [os.path.join(current_dir, file_name) for file_name in ['banned-ips.json', 'banned-players.json', 'bukkit.yml', 
                       'commands.yml', 'help.yml', 'ops.json', 'server.properties', 
                       'spigot.yml', 'usercache.json', 'whitelist.json', "purpur.yml", "pufferfish.yml", "permissions.yml",
                       "version_history.json"]]
    folders_to_delete = [os.path.join(current_dir, folder_name) for folder_name in ['bundler', 'logs', 'world', 'world_nether', 'world_the_end',"libraries", "versions", "cache", "config", "crash-reports"]]
    
    try:
        # Lösche die angegebenen Dateien
        for file_path in files_to_delete:
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"{os.path.basename(file_path)} wurde gelöscht.")
            else:
                logger.error(f"{os.path.basename(file_path)} existiert nicht im Zielverzeichnis.")
                
        # Überprüfe, ob das Plugin-Verzeichnis erfolgreich gelöscht wurde und erstelle es erneut
        if not os.path.exists(plugins):
            os.makedirs(plugins)
            logger.info(f"{plugins} wurde wieder erstellt.")
        
        # Lösche die angegebenen Ordner
        for folder_path in folders_to_delete:
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                logger.info(f"{os.path.basename(folder_path)} wurde gelöscht.")
            else:
                logger.error(f"{os.path.basename(folder_path)} existiert nicht im Zielverzeichnis.")
        
        logger.info("Alle Dateien und Ordner wurden erfolgreich gelöscht und wiederhergestellt.")
    
    except Exception as e:
        logger.critical(f"Fehler beim Löschen und Wiederherstellen der Dateien und Ordner: {e}")

        for folder_path in folders_to_delete:
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                logger.info(f"{os.path.basename(folder_path)} wurde gelöscht.")
            else:
                logger.error(f"{os.path.basename(folder_path)} existiert nicht im Zielverzeichnis.")
        
        logger.info("Alle Dateien und Ordner wurden erfolgreich gelöscht.")
    
    except Exception as e:
        logger.critical(f"Fehler beim Löschen der Dateien und Ordner: {e}")

def delete_files():
    logger.info("User pressed delete server files!")
    confirmation = messagebox.askyesno("Server Builder", "Are you sure that you want to continue? Your about to delete everything!")
    if not confirmation:
        logger.info("User cancelled!")
        return
    logger.info("User confirmed!")
    
    current_dir = os.path.dirname(os.path.realpath(__file__))
    plugins = os.path.join(current_dir, 'plugins')
    
    # Lösche das Plugin-Verzeichnis und seinen Inhalt
    try:
        shutil.rmtree(plugins)
        logger.info(f"The plugin directory {plugins} and its contents have been successfully deleted.")
    except Exception as e:
        logger.error(f"Error deleting the plugin directory and its contents: {e}")
    
    # Dateien und Ordner, die gelöscht und wiederhergestellt werden sollen
    files_to_delete = ['banned-ips.json', 'banned-players.json', 'bukkit.yml', 'commands.yml', 'help.yml', 'ops.json', 'server.properties', 'spigot.yml', 'usercache.json', 'whitelist.json', 'purpur.yml', 'pufferfish.yml', 'permissions.yml', 'version_history.json']
    folders_to_delete = ['bundler', 'logs', 'world', 'world_nether', 'world_the_end', 'libraries', 'versions', 'cache', 'config', 'crash-reports']
    
    try:
        # Lösche die angegebenen Dateien
        for file_name in files_to_delete:
            file_path = os.path.join(current_dir, file_name)
            if os.path.exists(file_path):
                os.remove(file_path)
                logger.info(f"The file {file_name} has been deleted.")
            else:
                logger.warning(f"The file {file_name} does not exist in the target directory.")
        
        # Überprüfe, ob das Plugin-Verzeichnis erfolgreich gelöscht wurde und erstelle es erneut
        if not os.path.exists(plugins):
            os.makedirs(plugins)
            logger.info(f"The plugin directory {plugins} has been recreated.")
        
        # Lösche die angegebenen Ordner
        for folder_name in folders_to_delete:
            folder_path = os.path.join(current_dir, folder_name)
            if os.path.exists(folder_path):
                shutil.rmtree(folder_path)
                logger.info(f"The folder {folder_name} has been deleted.")
            else:
                logger.warning(f"The folder {folder_name} does not exist in the target directory.")
        
        logger.info("All files and folders have been successfully deleted and restored.")
    
    except Exception as e:
        logger.error(f"Error deleting and restoring files and folders: {e}")
        
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


file_menu = tk.Menu(menubar, tearoff=0)
file_menu.add_command(label="Exit", command=root.quit)

def about():
    messagebox.showinfo("Server Builder", "No information given.")

def reset_config_and_restart():
    try:
        os.remove("config.ini")
        config.write_data()
        logger.info("Configuration file reset successful.")
        root.destroy()  # Schließe das aktuelle Fenster
        restart_program()  # Starte das Programm erneut
    except FileNotFoundError:
        logger.error("Configuration file not found.")
    except Exception as e:
        logger.error(f"Error resetting configuration file: {e}")

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)

# Edit menu
edit_menu = tk.Menu(menubar, tearoff=0)
edit_menu.add_command(label="Delete all server files", command=delete_server_files1)
edit_menu.add_command(label="Reset config.ini", command=reset_config_and_restart)
edit_menu.add_command(label="About", command=about)

# Add File and Edit menus to the menu bar
menubar.add_cascade(label="File", menu=file_menu)
menubar.add_cascade(label="Settings", menu=edit_menu)

def switch(indicator_lb, page):
    # Festlegen der Standardhintergrundfarbe
    default_bg_color = "SystemButtonFace"
    # Überprüfen, ob das Betriebssystem Linux ist
    if platform.system() == "Linux":
        # Verwenden einer alternativen Hintergrundfarbe für Linux
        default_bg_color = "grey"  # Hier die gewünschte alternative Farbe einsetzen
    
    # Ändern der Hintergrundfarbe aller Labels in options_fm
    for child in options_fm.winfo_children():
        if isinstance(child, tk.Label):
            child["bg"] = default_bg_color
    
    # Setzen der Hintergrundfarbe des ausgewählten Indikatorlabels auf Schwarz
    indicator_lb["bg"] = "black"
    
    # Löschen aller Widgets in main_fm, um Platz für die neue Seite zu machen
    for fm in main_fm.winfo_children():
        fm.destroy()
        root.update()  # Aktualisieren des Fensters, um die Änderungen anzuzeigen
    
    # Aufrufen der Funktion der neuen Seite, um sie anzuzeigen
    page()

options_fm = tk.Frame(root)

home_btn = tk.Button(options_fm, text="Home", font=("Open Sans", 15), bd=0, fg="black", activebackground="white", command=lambda: switch(indicator_lb=home_indicator_lb, page=home_page))
home_btn.place(x=0, y=0, width=125)
home_indicator_lb = tk.Label(options_fm, bg="black")
home_indicator_lb.place(x=22, y=32, width=80, height=2)

Launcher_btn = tk.Button(options_fm, text="Launcher", font=("Open Sans", 15), bd=0, fg="black", activebackground="white", command=lambda: switch(indicator_lb=Launcher_indicator_lb, page=launcher_page))
Launcher_btn.place(x=125, y=0, width=125)
Launcher_indicator_lb = tk.Label(options_fm)
Launcher_indicator_lb.place(x=147, y=32, width=80, height=2)

Software_btn = tk.Button(options_fm, text="Software", font=("Open Sans", 15), bd=0, fg="black", activebackground="white", command=lambda: switch(indicator_lb=Software_indicator_lb, page=software_page))
Software_btn.place(x=250, y=0, width=125)
Software_indicator_lb = tk.Label(options_fm)
Software_indicator_lb.place(x=277, y=32, width=80, height=2)

Plugins_btn = tk.Button(options_fm, text="Plugins", font=("Open Sans", 15), bd=0, fg="black", activebackground="white", command=lambda: switch(indicator_lb=Plugins_indicator_lb, page=plugins_page))
Plugins_btn.place(x=375, y=0, width=125)
Plugins_indicator_lb = tk.Label(options_fm)
Plugins_indicator_lb.place(x=392, y=32, width=80, height=2)

Discord_btn = tk.Button(options_fm, text="Discord", font=("Open Sans", 15), bd=0, fg="black", activebackground="white", command=lambda: switch(indicator_lb=Discord_indicator_lb, page=discord))
Discord_btn.place(x=500, y=0, width=125)
Discord_indicator_lb = tk.Label(options_fm)
Discord_indicator_lb.place(x=522, y=32, width=80, height=2)

options_fm.pack(pady=5)
options_fm.pack_propagate(False)
options_fm.configure(width=800, height=35)

def home_page():
    global main_fm
    home_frame = tk.Frame(main_fm)
    home_label = tk.Label(home_frame, text="Homepage", font=("Open Sans", 16), fg="black")
    home_label.pack(pady=80)
    home_frame.pack(fill=tk.BOTH, expand=True)

def plugins_page():
    global main_fm
    plugins_frame = tk.Frame(main_fm)
    plugins_label = tk.Label(plugins_frame, text="Plugins", font=("Open Sans", 16), underline=True)
    plugins_label.pack(pady=10)  # Zentriert die Beschriftung vertikal
    
    global listbox
    listbox = tk.Listbox(plugins_frame, bg="white", fg="blue", width=50, height=10)
    listbox.pack(pady=10)  # Zentriert die Liste vertikal
    
    create_button1 = tk.Button(plugins_frame, text="Add plugin", command=add_plugin, width=20)  # Buttonbreite erhöht
    create_button1.pack(pady=10)  
    
    create_button2 = tk.Button(plugins_frame, text="Remove plugin", command=remove_plugin, width=20)  # Buttonbreite erhöht
    create_button2.pack(pady=10)  
    
    # Zentriert das plugins_frame horizontal und vertikal
    plugins_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    
    plugins_frame.pack(fill=tk.BOTH, expand=True)

    def show_folder_contents():
        global listbox
        listbox.delete(0, tk.END)
        for item in os.listdir(directory_path):
            listbox.insert(tk.END, item)
        root.after(1000, show_folder_contents)
        
    show_folder_contents()
    
def remove_plugin():
    initial_dir = "plugins"  # Das Ausgangsverzeichnis für den filedialog
    file_path = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("Jar files", "*.jar")])
    if not file_path:  
        return
    
    try:
        os.remove(file_path)  
        logger.info("Plugin successfully removed:", os.path.basename(file_path))
    except Exception as e:
        logger.error("Error removing plugin:", e)

def add_plugin():  
    inital_dir = current_dir
    file_path = filedialog.askopenfilename(initialdir=inital_dir, filetypes=[("Jar files", "*.jar")])
    if file_path and os.path.isfile(file_path):
        plugins_folder = "plugins"
        if not os.path.exists(plugins_folder):
            os.makedirs(plugins_folder)
        try:
            shutil.copy(file_path, plugins_folder)
            logger.info("Plugin successfully added:", os.path.basename(file_path))
        except Exception as e:
            logger.error("Error adding plugin:", e)
    else:
        logger.info("No valid .jar file selected.")

def software_page():
    global main_fm

    for widget in main_fm.winfo_children():
        widget.destroy()

    software_frame = tk.Frame(main_fm)
    software_frame.grid(row=0, column=0, padx=50, pady=10)  # Hier haben wir padx angepasst

    tree = ttk.Treeview(software_frame, columns=("Name", "Download Link", "Release Date"), show="headings", selectmode="browse")
    tree.heading("Name", text="Name")
    tree.heading("Download Link", text="Download Link")
    tree.heading("Release Date", text="Release Date")
    tree.column("Name", width=200)
    tree.column("Download Link", width=340)
    tree.column("Release Date", width=100)
    tree.grid(row=0, column=0, columnspan=2, sticky="nsew")

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
    progress_bar = ttk.Progressbar(software_frame, orient="horizontal", length=200, mode="determinate", variable=progress_var)
    progress_bar.grid(row=1, column=0, columnspan=2, sticky="ew")

    def update_progress(percent):
        progress_var.set(percent)

    def start_download():
        selected_item = tree.focus()
        if not selected_item:
            messagebox.showerror("Error", "Please select a server version to download.")
            return

        values = tree.item(selected_item, "values")
        url = values[1]
        filename = "server.jar"
        build_directory = "Minecraft_jar_file"
        file_path = os.path.join(build_directory, filename)

        download_thread = threading.Thread(target=download_file, args=(url, file_path))
        download_thread.start()

    def download_file(url, file_path):
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

    start_button = tk.Button(software_frame, text="Start Download", command=start_download)
    start_button.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10, padx=50)  # Hier haben wir padx angepasst


def launcher_page():
    def create_eula_file():
        file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "eula.txt")
        try:
            with open(file_path, 'w') as file:
                file.write("eula=true\n")
                logger.info(f"EULA file successfully created: {file_path}")
        except FileNotFoundError:
            logger.error("The file 'eula.txt' does not exist.")
        except PermissionError:
            logger.error("No permission to create the file 'eula.txt'.")
        except Exception as e:
            logger.error(f"Error creating the EULA file: {e}")

    def start_server():
        ram_value = int(ram_var.get())
        ram_value_str = f"{ram_value}G"
        logger.info("Starting the server with RAM value: %s", ram_value_str)
        start_download = threading.Thread(target=os.system, args=(f"java -Xmx{ram_value_str} -jar Minecraft_jar_file/server.jar",))
        start_download.start()

    def check_jar_file():
        jar_file_path = "Minecraft_jar_file/server.jar"
        if not os.path.exists(jar_file_path):
            start_button.config(state=tk.DISABLED)
            jar_message_label.config(text="Please download the server.jar file.")
        else:
            start_button.config(state=tk.NORMAL)
            jar_message_label.config(text="")
            check_eula()

    def check_eula():
        eula_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "eula.txt")
        if os.path.exists(eula_file_path):
            with open(eula_file_path, 'r') as file:
                eula_content = file.read().strip()
            if "eula=true" in eula_content:
                start_button.config(state=tk.NORMAL)
                eula_message_label.config(text="")
                return True
            else:
                start_button.config(state=tk.DISABLED)
                eula_message_label.config(text="Please accept the EULA to start the server.")
                return False
        else:
            start_button.config(state=tk.DISABLED)
            eula_message_label.config(text="Please accept the EULA to start the server.")
            return False

    def on_start_button_click():
        logger.info("Checking if the EULA is already accepted.")
        if not check_eula():
            logger.info("Opening a dialog to accept the EULA.")
            messagebox12 = messagebox.askyesno("Server Builder", "By starting the server, you accept the Minecraft End User License Agreement.")
            if not messagebox12:  
                logger.info("User did not accept the EULA.")
                return
            create_eula_file()
        start_server()

    launcher_frame = tk.Frame(main_fm)

    ttk.Label(launcher_frame, text="RAM Allocation (GB):").pack()

    ram_var = tk.DoubleVar()
    ram_scale = Scale(launcher_frame, from_=1, to=Max_RAM, orient=tk.HORIZONTAL, variable=ram_var, length=200, width=20)
    ram_scale.pack()

    start_button = ttk.Button(launcher_frame, text="Start Server", command=on_start_button_click)
    start_button.pack()

    eula_message_label = ttk.Label(launcher_frame, text="")
    eula_message_label.pack()

    jar_message_label = ttk.Label(launcher_frame, text="")
    jar_message_label.pack()

    launcher_frame.pack(fill=tk.BOTH, expand=True)

    check_jar_file()



def discord():
    global main_fm
    discord_frame = tk.Frame(main_fm)
    discord_label = tk.Label(discord_frame, text="Opening Discord...", font=("Open Sans", 16), fg="black")
    discord_label.pack(pady=80)
    discord_frame.pack(fill=tk.BOTH, expand=True)
    webbrowser.open_new_tab("https://discord.gg/Z4x6Z5eT7Q")

main_fm = tk.Frame(root)
main_fm.pack(fill=tk.BOTH, expand=True)
home_page()

root.mainloop()
