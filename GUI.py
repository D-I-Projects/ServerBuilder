from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sys

def exit():
    if messagebox.askyesno(title="Exit?", message="Are You Shure,S That You Want To Exit?"):
        sys.exit(0)

def no_feature():
    messagebox.showinfo(title="No Feature", message="This Is An Feature That Isn't Implementet Yet!")

def do_you_like_to_continue():
    if messagebox.askyesno(title="Continue", message="Do You Want To Continue? In This Version You Can't Change Anything After Building!"):
        no_feature()


root = Tk()
root.title("MC Server Builder")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Button(mainframe, text="Exit", command=exit).grid(column=1, row=1, sticky=W)
ttk.Button(mainframe, text="Start", command=do_you_like_to_continue).grid(column=2, row=1, sticky=W)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.mainloop()
