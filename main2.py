import os, sys
import requests
import sqlite3
from tkinter import *

class Hystats():

    def get_stats(self, file):
        api_key = self.get_api_key()
        if not api_key:
            print('API key not found! Please create a new one using /api key.')
            print('Could not update stats and member list: API key not set.')
            return
        
        if requests.get(f"https://api.hypixel.net/player?key={api_key}&name=tatyanesimp").json()['cause'] == 'Invalid API key':
            print('API key invalid! Please create a new one using /api key.\nCould not update stats and member list: API key invalid.')
            return

        if not self.manualtext.get():
            line = self.get_online(file)
            if line:
                players = line.split(',')
            else:
                print('Please run /who to update member list!')
                return
        else:
            players = self.manualtext.get().split(',')

        for i in players:
            data = requests.get(f"https://api.hypixel.net/player?key={api_key}&name={i}").json()
            

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
            print('API key recieved!')
    
    def get_new_api_key(self, file):
        readline = file.seek(0,2)
        for line in file:
            if "[Client thread/INFO]: [CHAT] Your new API key is" in line:
                recieve_api_key(line[61:])
            else:
                continue

        self.apikeysuccess = Label(self.root, text='Couldn\'t find an API key! Try running /api new!')
        self.apikeysuccess.grid(row=3, column=1)

    def get_online(self, file):
        file.seek(0,2)
        for line in file:
            line = file.readline()
            if "[Client thread/INFO]: [CHAT] ONLINE:" in line:
                return line[49:]
            else:
                continue

    def get_running_minecraft_instance(self):
        pass

run = Hystats()

run.root.mainloop()