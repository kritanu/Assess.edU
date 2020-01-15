import sys
import os
from tkinter import *

window=Tk()

window.title("Running Python Script")
window.geometry('550x200')

def run():
    os.system('python compare.py')

btn = Button(window, text="GRADE IT!", bg="black", fg="white",command=run,height="20", width="100")
#btn.grid(column=, row=0)
btn.pack()

window.mainloop()