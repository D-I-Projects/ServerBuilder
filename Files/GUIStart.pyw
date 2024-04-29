from tkinter import *
from tkinter import ttk
import os
import sys
from tkinter.ttk import Style
import subprocess

#Mainframe
root = Tk()
root.title("Server Builder")
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.geometry("250x85")
icon_image = PhotoImage(file="icon.png")
root.wm_iconphoto(True, icon_image)
style = ttk.Style()

style.configure("Normal.TButton", 
                foreground="white", 
                background="blue", 
                font=("Helvetica", 12), 
                padding=10)

for Arg in sys.argv:
    print(Arg)
    if "-developer=true" == Arg:
        developer_mode = True
    else:
        developer_mode = False

def setup_server():
    root.destroy()
    subprocess.Popen(["pythonw", "GUISetupServer.pyw"])

def launch_server():
    root.destroy()
    subprocess.Popen(["pythonw", "GUILaunchServer.pyw"])
    
def settings():
    root.destroy()
    subprocess.Popen(["pythonw", "GUISettings.pyw"])

ttk.Button(mainframe, text="Launch-Server", command=launch_server).grid(column=0, row=0, sticky=W)
ttk.Button(mainframe, text="Setup-Server", command=setup_server).grid(column=0, row=1, sticky=W)
ttk.Button(mainframe, text="Settings", command=settings).grid(column=0, row=2, sticky=W)

root.mainloop()

input("Press Enter to exit...")

