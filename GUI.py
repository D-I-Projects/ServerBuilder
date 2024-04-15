from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sys
messagebox.YES = 'yes'
def exit():
    if messagebox.askyesno(title="Exit?", message="Are You Shure That You Want To Exit?"):
        sys.exit(0)

def no_feature():
    messagebox.showinfo(title="No Feature", message="This Is An Feature That Isn't Implementet Yet!")


root = Tk()
root.title("MC Server Builder")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

ttk.Button(mainframe, text="Exit", command=exit).grid(column=1, row=1, sticky=W)
ttk.Button(mainframe, text="Start", command=no_feature).grid(column=2, row=1, sticky=W)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

root.mainloop()
