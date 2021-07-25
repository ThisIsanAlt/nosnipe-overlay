from threading import Thread
from tkinter import *
import time
root = Tk()

def move_window(event):
    root.geometry('+{0}+{1}'.format(event.x_root, event.y_root))

def init(root):
    root.geometry("1000x500+50+50")
    root.attributes('-alpha', 0.8)
    root.wm_attributes("-topmost", True)
    root.resizable(False, False)
    root['background'] = '#000000'

    root.overrideredirect(True)


    title_bar = Frame(root, bg='white', relief='raised', bd=2, width=1000)

    # put a close button on the title bar
    close_button = Button(title_bar, text='X', command=root.destroy)

    # pack the widgets
    title_bar.grid(row=0, column=0, padx=(980, 1), pady=1)
    close_button.pack(side=RIGHT)

    # bind title bar motion to the move window function
    title_bar.bind('<B1-Motion>', move_window)

    # menubar = Frame(root, bd=0, highlightthickness=0, bg='#222222', height=25, width=1000)
    # menubar.grid(row=0, column=0, sticky=W)

    # bwbutton = Button(menubar, font=('Calibri'), text='Bedwars')
    # bwbutton.grid(row=0, column=0, sticky=W, padx=(10,0))

    # bridgebutton = Button(menubar, font=('Calibri'), text='Bridge')
    # bridgebutton.grid(row=0, column=1, sticky=W)

    # uhcdbutton = Button(menubar, font=('Calibri'), text='UHCDuels')
    # uhcdbutton.grid(row=0, column=2, sticky=W)

    # swbutton = Button(menubar, font=('Calibri'), text='Skywars')
    # swbutton.grid(row=0, column=3, sticky=W, padx=(0,843))

    # a canvas for the main area of the window
    terminal = Frame(root, bd=0, highlightthickness=0, bg='black', height=400, width=1000)
    terminal.grid(row=1, column=0, sticky=SW)

    initLabelDuels(terminal)

def initLabelDuels(terminal):
    playerlabel = Label(terminal, font=('Calibri',20), text='PLAYER', bg='black', fg='white', padx=100, pady=1)
    playerlabel.grid(row=0, column=0, sticky=W)

    taglabel = Label(terminal, font=('Calibri',20), text='TAG', bg='black', fg='white', padx=20, pady=1)
    taglabel.grid(row=0, column=1, sticky=W)

    wslabel = Label(terminal, font=('Calibri',20), text='WS', bg='black', fg='white', padx=20, pady=1)
    wslabel.grid(row=0, column=2, sticky=W)

    kdrlabel = Label(terminal, font=('Calibri',20), text='KDR', bg='black', fg='white', padx=20, pady=1)
    kdrlabel.grid(row=0, column=3, sticky=W)

    wlrlabel = Label(terminal, font=('Calibri',20), text='WLR', bg='black', fg='white', padx=20, pady=1)
    wlrlabel.grid(row=0, column=4, sticky=W)

    killslabel = Label(terminal, font=('Calibri',20), text='KILLS', bg='black', fg='white', padx=20, pady=1)
    killslabel.grid(row=0, column=5, sticky=W)

    playerlabel = Label(terminal, font=('Calibri',20), text='WINS', bg='black', fg='white', padx=20, pady=1)
    playerlabel.grid(row=0, column=6, sticky=W)

    
def reposition():
    while True:
        time.sleep(0.1)
        root.geometry('+50+50')

if __name__ == "__main__":
    thread2 = Thread(target = init, args=(root,))
    thread = Thread(target = reposition)
    thread2.start()
    thread.start()

    root.mainloop()