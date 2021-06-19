from threading import Thread
from tkinter import *
import time
root = Tk()

version = "0.0.2[ALPHA]"

def init():
    global root
    root.geometry("1000x500+50+50")
    root.attributes('-alpha', 0.8)
    root.lift()
    root.wm_attributes("-topmost", True)
    root.resizable(False, False)
    menubar = Frame(root, bd=0, highlightthickness=0, bg='white', height=20, width=1000)
    menubar.grid(row=0, column=0)

    # a canvas for the main area of the window
    terminal = Frame(root, bd=0, highlightthickness=0, bg='black', height=480, width=1000)

    # pack the widgets
    terminal.grid(row=1, column=0)

    # bind title bar motion to the move window function
    
    
def reposition():
    while True:
        time.sleep(0.1)
        root.geometry('+50+50')

if __name__ == "__main__":
    thread2 = Thread(target = init)
    thread = Thread(target = reposition)
    thread2.start()
    thread.start()

    root.mainloop()
