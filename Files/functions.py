import os
import configparser
import logging
import datetime
def log_settings():
    log_dir = "ServerBuilder_Log"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    log_filename = os.path.join(log_dir, f"Server_Builder_functions.py - {current_datetime}.log")

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

logger.info("functions.py was loaded!")

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
