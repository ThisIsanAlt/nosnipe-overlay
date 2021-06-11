import os, sys
import requests
import sqlite3
from tkinter import *
import threading

class Hystats():

    def __init__(self):
        self.root = Tk()

        self.title = Label(self.root, text='Hypixel Stats Overlay v0.1.0 [BETA]')
        self.title.grid(row=0,column=1)

        self.statsbutton = Button(self.root, text='Get stats!', command=threading.Thread(target=self.get_stats(open(os.path.join(sys.path[0], "test.txt"))).start()))
        self.statsbutton.grid(row=2, column=0)
        #self.statsbutton = Button(self.root, text='Get stats!', command=threading.Thread(target=self.get_stats(open(os.getenv("APPDATA")+"/.minecraft/logs/blclient/minecraft/latest.log", "r"))).start())

        self.manualtext = Label(self.root, text='Manual Search: Leave empty for auto checking')
        self.manualtext.grid(row=1,column=0)

        self.playerent = Entry(self.root)
        self.playerent.grid(row=1,column=1)

        #self.apikeybutton = Button(self.root, text='Register new API key!', command=threading.Thread(target=self.get_new_api_key(open(os.getenv("APPDATA")+"/.minecraft/logs/blclient/minecraft/latest.log", "r"))).start())
        self.apikeybutton = Button(self.root, text='Register new API key!', command=threading.Thread(target=self.get_new_api_key(open(os.path.join(sys.path[0], "test.txt"))).start()))
        self.apikeybutton.grid(row=3, column=0)

    def get_stats(self, file):
        api_key = self.get_api_key()

        line = self.get_online(file)
        if line:
            players = line.split(',')
        else:
            print('Please run /who to update member list!')
    
        if not api_key:
            print('API key not found! Please create a new one using /api key.')
            print('Could not update stats and member list: API key not set.')
            return

        if requests.get(f"https://api.hypixel.net/player?key={api_key}&name=tatyanesimp").json()['success']:
            print('Success:', requests.get(f"https://api.hypixel.net/player?key={api_key}&name=tatyanesimp").json()['success'])
            print('API key invalid! Please create a new one using /api key.\nCould not update stats and member list: API key invalid.')
            return

        #for i in players:
        #    data = requests.get(f"https://api.hypixel.net/player?key={api_key}&name={i}").json()

    def get_api_key(self):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        data = c.execute('SELECT APIKey FROM KEYS')
        data = data.fetchone()
        return data[0][0]
            
    def recieve_api_key(self, api_key):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            c.execute(f'UPDATE KEYS SET APIKey = "{api_key}"')
        except Exception:
            c.execute('CREATE TABLE KEYS(APIKey)')
            c.execute(f'INSERT INTO KEYS(APIKey) VALUES ("{api_key}")')
        finally:
            c.commit()
            print('API key recieved and logged!')

    def get_online(self, file):
        file.seek(0,2)
        for line in file:
            line = file.readline()
            if "[Client thread/INFO]: [CHAT] ONLINE:" in line:
                return line[49:]
            else:
                continue

    def get_new_api_key(self, file):
        readline = file.seek(0,2)
        for line in file:
            if "[Client thread/INFO]: [CHAT] Your new API key is" in line:
                recieve_api_key(line[61:])
            else:
                continue

    def get_running_minecraft_instance(self):
        pass

run = Hystats()

inputa=input('')