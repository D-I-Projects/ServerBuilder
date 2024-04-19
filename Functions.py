def no_feature(messagebox, title="No Feature", message="This Is An Feature That Isn't Implementet Yet!"):
    messagebox.showinfo(title=title, message=message)
   # print(int(provider_listbox.curselection()[-1]))

def update_code(os, root, programm="./GUI.py", developer=False):
    root.destroy()
    os.system(f"python3 {programm} -developer={str(developer).lower()}")

def exit(sys, messagebox, title="Exit?", message="Are You Shure That You Want To Exit?"):
    if messagebox.askyesno(title=title, message=message):
        sys.exit(0)

def do_you_like_to_continue_afterbuild(messagebox, function, title="Continue", message="Do you want To continue? After the download is succeded the file will be inside the program folder!"):
    if messagebox.askyesno(title=title, message=message):
        function()

def set_settings_setup_server(root, provider_listbox, mainframe, N, W, E, S):
    root.title("MC Server Builder")

    provider_listbox.grid(column=0, row=2)
    provider_listbox.selection_set(0)
    
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

def do_you_like_to_continue_only_if_installed_serverjar(messagebox, function, title="Continue", message="Do you want to continue? If you didn't executed Setup-Server before, nothing will happen!"):
    if messagebox.askyesno(title=title, message=message):
        function()

def no_selection(messagebox, title="No Selection", message="No selection for server systems!"):
    messagebox.showinfo(title=title, message=message)

def server_launching():
    pass
