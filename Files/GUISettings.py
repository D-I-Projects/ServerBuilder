from tkinter import *
from tkinter import ttk
import os
from tkinter import ttk
import subprocess
import logging
import datetime
import shutil
from tkinter import messagebox

def log_settings():
    log_dir = "ServerBuilder_Log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = os.path.join(log_dir, f"Server_Builder_GUISettings - {current_datetime}.log")

    logger = logging.getLogger("ServerBuilder_GUISettings")
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

logger.info("GUISettings.py was opened!")

#Mainframe
root = Tk()
root.title("Settings")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
icon_image = PhotoImage(file="sbicon.png")
root.wm_iconphoto(True, icon_image)


window_text = ttk.Label(mainframe, text="Settings", font=("Open Sans", 16), underline=True)
window_text.grid(column=0, row=0, sticky=W)

window_text = ttk.Label(mainframe, text="Other", font=("Open Sans", 12))
window_text.grid(column=0, row=4, sticky=W)

#Define Functions
def back():
    logger.info("User pressed back...")
    root.destroy()
    subprocess.Popen(["python3", "GUIStart.py"])
    
def program_information():
    logger.info("User pressed program informations...")
    root.destroy()
    subprocess.Popen(["python3", "GUIProgramInformation.py"])
    
def contact():
    logger.info("User pressed contacts...")
    root.destroy()
    subprocess.Popen(["python3", "GUIContact.py"])
    
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
        
  
def create_buttons():
    ttk.Button(mainframe, text="Back", command=back).grid(column=0, row=5, sticky=W)
    ttk.Button(mainframe, text="Program Informations", command=program_information).grid(column=0, row=1, sticky=W)
    ttk.Button(mainframe, text="Contacts", command=contact).grid(column=1, row=1, sticky=W)
    ttk.Button(mainframe, text="Delete ALL Server files", command=delete_server_files1).grid(column=2, row=1, sticky=W)


#Create Buttons
create_buttons()

#Starting Mainloop
root.mainloop()

input("Press Enter to exit...")
