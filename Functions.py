def no_feature(messagebox, title="No Feature", message="This Is An Feature That Isn't Implementet Yet!"):
    messagebox.showinfo(title=title, message=message)
   # print(int(provider_listbox.curselection()[-1]))

def update_code(os, root, programm="./GUI.py", developer=False):
    root.destroy()
    os.system(f"python3 {programm} -developer={str(developer).lower()}")

def exit(sys, messagebox, title="Exit?", message="Are You Shure That You Want To Exit?"):
    if messagebox.askyesno(title=title, message=message):
        sys.exit(0)

#def do_you_like_to_continue(messagebox, function, title="Continue", message="Do You Want To Continue? In This Version You Can't Change Anything After Building!"):
 #   if messagebox.askyesno(title=title, message=message):
    #    function()

def set_settings_setup_server(root, provider_listbox, mainframe, N, W, E, S):
    root.title("MC Server Builder")

    provider_listbox.grid(column=0, row=2)
    provider_listbox.selection_set(0)
    
    mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
