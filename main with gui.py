import os
from os import system, sys
import platform
from colorama import Fore
import requests
import sqlite3
import math
import asyncio
loop = asyncio.get_event_loop()
system("color")
from tkinter import *
import threading

'TABLE INFO(APIKey, CriticalWins, WarningWins, CriticalNWLVL, WarningNWLVL)'

class Hystats():

    def __init__(self):  # sourcery skip: remove-redundant-if
        self.version = "0.0.2[ALPHA]"

        self.root = Tk()
        self.root.attributes('-alpha', 0.5)
        self.root.lift()

        meta = requests.get(f"https://thisisanalt.github.io/data/basic_info.json").json()
        self.blacklist = meta['blacklist']
        if meta['version'] != self.version:
            pass
        if self.version in meta['version-blacklist']:
            pass

        self.title = Label(self.root, text=f'NoSnipe Overlay {self.version}')
        self.title.grid(row=0,column=1)

        self.uuids = {}        
        
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            if len(c.execute('SELECT CriticalWins FROM INFO').fetchall()) == 0:
                pass
        except:
            c.execute('CREATE TABLE INFO(APIKey, CriticalWins, WarningWins, CriticalNWLVL, WarningNWLVL)')
        self.params = c.execute('SELECT * FROM INFO').fetchone()
        conn.close()

    def getAPIKey(self,):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        data = c.execute('SELECT APIKey FROM INFO')
        data = data.fetchone()
        conn.close()
        try:
            return data[0]
        except:
            return
            
    def recieve_api_key(self, api_key):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            c.execute(f'UPDATE INFO SET APIKey = "{api_key}"')
        except Exception:
            c.execute(f'INSERT INTO INFO(APIKey) VALUES ("{api_key}")')
        finally:
            c.commit()
            print('API key recieved!')
            conn.close()

    async def readFile(self, thefile):
        autocheck = True
        input('Press ENTER once connected to Hypixel.')
        print(f'Autocheck {Fore.LIGHTGREEN_EX}ACTIVE{Fore.RESET}')
        thefile.seek(0,2)
        while True:
            line = thefile.readline()
            if not line:
                asyncio.sleep(0.1)
            if autocheck:
                if ("[Client thread/INFO]: [CHAT]" and "has joined") in line:
                    player = line[40:].split(' ')[0]
                    await self.getStats(player)
                elif "[Client thread/INFO]: [CHAT] Your new API key is" in line:
                    self.recieve_api_key(line[61:])
                elif ("[Client thread/INFO]: [CHAT] Sending you to") in line:
                    if 'windows' in platform.system().lower():
                        self.system('cls')
                    if self.mode == 'bridge':
                        await self.printBridgeTable()
                    elif self.mode == 'bw':
                        await self.printBWTable()
            elif ("[Client thread/INFO]: [CHAT] Connecting to") in line:
                if "hypixel" not in line:
                    print(f'Autocheck {Fore.LIGHTRED_EX}INACTIVE{Fore.RESET}')
                else:
                    print(f'Autocheck {Fore.LIGHTGREEN_EX}ACTIVE{Fore.RESET}')
    
    async def getStats(self, player):
        global uuids
        global mode
        api_key = self.getAPIKey()

        if player not in self.uuids:
            try:
                uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player}").json()['id']
            except:
                print(f'IGN {player} not found, player is most likely nicked')
                return
            self.uuids[player] = uuid
        else:
            uuid = self.uuids.get(player)
        data = requests.get(f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}").json()

        if not data['success']:
            print(data['cause'])
            return
        elif self.mode == 'bridge':
            await self.getBridgeStats(data, uuid)
        elif self.mode == 'bw':
            await self.getBWStats(data, uuid)
        
    def getDuelsPrestigeMode(self, wins):
        if wins < 50:
            return wins
        elif wins < 100:
            return f'{Fore.LIGHTBLACK_EX}{wins}{Fore.RESET}'
        elif wins < 200:
            return f'{Fore.RESET}{wins}'
        elif wins < 500:
            return f'{Fore.YELLOW}{wins}{Fore.RESET}'
        elif wins < 1000:
            return f'{Fore.CYAN}{wins}{Fore.RESET}'
        elif wins < 2000:
            return f'{Fore.GREEN}{wins}{Fore.RESET}'
        elif wins < 5000:
            return f'{Fore.RED}{wins}{Fore.RESET}'
        elif wins < 10000:
            return f'{Fore.LIGHTYELLOW_EX}{wins}{Fore.RESET}'
        else:
            return f'{Fore.MAGENTA}{wins}{Fore.RESET}'

    async def getBridgeStats(self, data, uuid):
        global params
        global blacklist
        try:
            name = data['player']['display_name'] 
        except:
            name = data['player']['playername']
        wins = data['player']['stats']['Duels'].get('bridge_duel_wins', 0) + data['player']['stats']['Duels'].get('bridge_doubles_wins', 0) \
            + data['player']['stats']['Duels'].get('bridge_four_wins', 0) + data['player']['stats']['Duels'].get('bridge_2v2v2v2_wins', 0) + data['player']['stats']['Duels'].get('bridge_3v3v3v3_wins', 0)
        
        losses = data['player']['stats']['Duels'].get('bridge_duel_losses', 0) + data['player']['stats']['Duels'].get('bridge_doubles_losses', 0) \
            + data['player']['stats']['Duels'].get('bridge_four_losses', 0) + data['player']['stats']['Duels'].get('bridge_2v2v2v2_losses', 0) + data['player']['stats']['Duels'].get('bridge_3v3v3v3_losses', 0)

        wlr = wins/losses    
        networkLevel = (math.sqrt((2 * data['player']['networkExp']) + 30625) / 50) - 2.5
        ws = data['player']['stats']['Duels']['current_bridge_winstreak']
        cage = data['player']['stats']['Duels']['active_cage'][5:]
        prestige = self.getDuelsPrestigeMode(wins)
        
        if uuid in self.blacklist:
            print(f'''        {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}
            {name} | {prestige} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} | {cage}
            {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}''')
        elif wins < self.params[1] or networkLevel < self.params[3]:
            print(f'''        {Fore.RED}---------------------CRITICAL---------------------{Fore.RESET}
            {name} | {prestige} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} | {cage}
            {Fore.RED}---------------------CRITICAL---------------------{Fore.RESET}''')
        elif wins < self.params[2] or networkLevel < self.params[4]:
            print(f'''        {Fore.YELLOW}---------------------WARNING---------------------{Fore.RESET}
            {name} | {prestige} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} | {cage}
            {Fore.YELLOW}---------------------WARNING---------------------{Fore.RESET}''')
        else:
            print(f'         {name} | {prestige} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} | {cage}')

    def getBWPrestige(self, star):
        if star < 100:
            return f'{Fore.LIGHTBLACK_EX}{star}{Fore.RESET}'
        elif star < 200 or (star < 1200 and star > 1100):
            return star
        elif star < 300 or (star < 1300 and star > 1200):
            return f'{Fore.YELLOW}{star}{Fore.RESET}'
        elif star < 400 or (star < 1400 and star > 1300):
            return f'{Fore.CYAN}{star}{Fore.RESET}'
        elif star < 500 or (star < 1500 and star > 1400):
            return f'{Fore.GREEN}{star}{Fore.RESET}'
        elif star < 600 or (star < 1600 and star > 1500):
            return f'{Fore.CYAN}{star}{Fore.RESET}'
        elif star < 700 or (star < 1700 and star > 1600):
            return f'{Fore.RED}{star}{Fore.RESET}'
        elif star < 800 or (star < 1800 and star > 1700):
            return f'{Fore.LIGHTMAGENTA_EX}{star}{Fore.RESET}'
        elif star < 900 or (star < 1900 and star > 1800):
            return f'{Fore.BLUE}{star}{Fore.RESET}'
        elif star < 1000:
            return f'{Fore.MAGENTA}{star}{Fore.RESET}'
        elif star < 1100:
            star = str(star)
            return f'{Fore.RED}{star[0]}{Fore.YELLOW}{star[1]}{Fore.LIGHTGREEN_EX}{star[2]}{Fore.CYAN}{star[3]}{Fore.RESET}'
        elif star < 2000:
            return f'{Fore.MAGENTA}{star}{Fore.RESET}'
        elif star < 2100:
            star = str(star)
            return f'{Fore.LIGHTBLACK_EX}{star[0]}{Fore.RESET}{star[1]}{star[2]}{Fore.LIGHTBLACK_EX}{Fore.RESET}'
        elif star < 2200:
            star = str(star)
            return f'{star[0]}{Fore.LIGHTYELLOW_EX}{star[1]}{star[2]}{star[3]}{Fore.RESET}'
        elif star < 2300:
            star = str(star)
            return f'{Fore.YELLOW}{star[0]}{Fore.RESET}{star[1]}{star[2]}{Fore.CYAN}{star[4]}{Fore.RESET}'

    async def getBWStats(self, data, uuid):
        global params
        global blacklist
        try:
            name = data['player']['display_name'] 
        except:
            name = data['player']['playername']
        
        #start prestige search while other data is being calculated
        star = data['player']['achievements']['bedwars_level']
        prestige = self.getBWPrestige(star)

        wins = data['player']['stats']['Bedwars'].get('eight_one_wins_bedwars', 0) + data['player']['stats']['Bedwars'].get('eight_two_wins_bedwars', 0) \
            + data['player']['stats']['Bedwars'].get('four_three_wins_bedwars', 0)  + data['player']['stats']['Bedwars'].get('four_four_wins_bedwars', 0)

        losses = data['player']['stats']['Bedwars'].get('eight_one_losses_bedwars', 0) + data['player']['stats']['Bedwars'].get('eight_two_losses_bedwars', 0) \
            + data['player']['stats']['Bedwars'].get('four_three_losses_bedwars', 0)  + data['player']['stats']['Bedwars'].get('four_four_losses_bedwars', 0)

        wlr = wins/losses    
        networkLevel = (math.sqrt((2 * data['player']['networkExp']) + 30625) / 50) - 2.5
        ws = data['player']['stats']['Bedwars']['winstreak']
        
        if uuid in self.blacklist:
            print(f'''      {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}
            {name} | {prestige} | {wins} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} 
            {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}''')
        elif wins < self.params[1] or networkLevel < self.params[3]:
            print(f'''      {Fore.RED}---------------------CRITICAL---------------------{Fore.RESET}
            {name} | {prestige} | {wins} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} 
            {Fore.RED}---------------------CRITICAL---------------------{Fore.RESET}''')
        elif wins < self.params[2] or networkLevel < self.params[4]:
            print(f'''      {Fore.YELLOW}---------------------WARNING---------------------{Fore.RESET}
            {name} | {prestige} | {wins} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} 
            {Fore.YELLOW}---------------------WARNING---------------------{Fore.RESET}''')
        else:
            print(f'         {name} | {prestige} | {wins} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} ')

    async def printBridgeTable(self):
        self.printTitle()
        title = f'''
            IGN    | Wins | WLR | NW LVL | WS | Active Cage
            '''
        print(title)

    async def printBWTable(self):
        self.printTitle()
        title = f'''
            IGN    |  ☆  | Wins | WLR | NW LVL | WS 
            '''
        print(title)

    def printTitle(self):
        title = f'''
            {Fore.CYAN}┌────────────────────────────────────────────────────────────┐
            {Fore.CYAN}│  {Fore.RESET}███╗   ██╗ ██████╗ {Fore.BLUE}███████╗███╗   ██╗██╗██████╗ ███████╗  {Fore.CYAN}│
            {Fore.CYAN}│  {Fore.RESET}████╗  ██║██╔═══██║{Fore.BLUE}██╔════╝████╗  ██║██║██╔══██╗██╔════╝  {Fore.CYAN}│
            {Fore.CYAN}│  {Fore.RESET}██╔██╗ ██║██║   ██║{Fore.BLUE}███████╗██╔██╗ ██║██║██████╔╝█████╗    {Fore.CYAN}│
            {Fore.CYAN}│  {Fore.RESET}██║╚██╗██║██║   ██║{Fore.BLUE}╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝    {Fore.CYAN}│
            {Fore.CYAN}│  {Fore.RESET}██║ ╚████║╚██████╔╝{Fore.BLUE}███████║██║ ╚████║██║██║     ███████╗  {Fore.CYAN}│
            {Fore.CYAN}│  {Fore.RESET}╚═╝  ╚═══╝ ╚═════╝ {Fore.BLUE}╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝  {Fore.CYAN}│
            {Fore.CYAN}└────────────────────────────────────────────────────────────┘
                                                                Overlay by sweting{Fore.RESET}'''
        print(title)

    def get_running_minecraft_instance(self):
        pass

run = Hystats()

inputa=input('')

