import os
import subprocess

def no_feature(messagebox, title="No feature", message="This is a feature that isn't Implementet yet!"):
    messagebox.showinfo(title=title, message=message)
   # print(int(provider_listbox.curselection()[-1]))

def exit(sys, messagebox, title="Exit?", message="Are you sure that you want to exit?"):
    if messagebox.askyesno(title=title, message=message):
        sys.exit(0)

def do_you_like_to_continue_afterbuild(messagebox, download_function):
    result = messagebox.askquestion("Continue", "Do you want to start the download?", icon='warning') 
    if result == 'yes':
        download_function()
    else:
        messagebox.showinfo("Cancelled", "Download cancelled.")

def set_settings_setup_server(root, provider_listbox, mainframe, N, W, E, S):
    provider_listbox.grid(column=0, row=2)
    provider_listbox.selection_set(0)
    
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

def do_you_like_to_continue_only_if_installed_serverjar(messagebox, function, title="Continue", message="Do you want to continue? If you didn't executed Setup-Server before, nothing will happen! Please also make sure you DO NOT have two different jar files in your folder!"):
    if messagebox.askyesno(title=title, message=message):
        function()
        
def accepting_eula(messagebox, function, title="Accepting eula!", message="With pressing yes your accepting the eula of Minecraft. The accepted eula is located inside eula.txt.", icon="warning"):
    if messagebox.askyesno(title=title, message=message):
        function()

def no_selection(messagebox, title="No Selection", message="No selection for server Systems!"):
    messagebox.showinfo(title=title, message=message)

def server_launching():
    subprocess.run (f"python3 ServerLauncher.pyw")