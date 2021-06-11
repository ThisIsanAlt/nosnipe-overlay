import time, os
from os import system
import platform
from colorama import Fore
import requests
import sqlite3
import math

'TABLE INFO(APIKey, CriticalWins, WarningWins, CriticalNWLVL, WarningNWLVL)'

def recieve_api_key(api_key):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        try:
            c.execute(f'UPDATE INFO SET APIKey = "{api_key}"')
        except Exception:
            c.execute('CREATE TABLE INFO(APIKey)')
            c.execute(f'INSERT INTO INFO(APIKey) VALUES ("{api_key}")')
        finally:
            c.commit()
            print('API key recieved!')
            conn.close()

def get_api_key():
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        data = c.execute('SELECT APIKey FROM INFO')
        data = data.fetchone()
        print(data)
        conn.close()
        try:
            return data[0]
        except:
            return

#implement 2v2v2v2 support
def getStats(player):
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        data = c.execute('SELECT * FROM INFO').fetchone()
        criticalWins = data[1]
        warningWins = data[2]
        criticalNWLVL = data[3]
        warningNWLVL = data[4]
        api_key = get_api_key()
        print(api_key+'+APIKEY')

        data = requests.get(f"https://api.hypixel.net/player?key={api_key}&name={player}").json()

        if not data['success']:
            print(data['cause'])
            return
        else:
            try:
                name = data['player']['display_name'] 
            except:
                name = data['player']['playername']
            wins = data['player']['stats']['Duels']['bridge_duel_wins'] + data['player']['stats']['Duels']['bridge_doubles_wins'] \
                + data['player']['stats']['Duels']['bridge_four_wins']  + data['player']['stats']['Duels']['bridge_3v3v3v3_wins']
            wlr = wins/data['player']['stats']['Duels']['bridge_duel_losses'] + data['player']['stats']['Duels']['bridge_doubles_losses'] \
                + data['player']['stats']['Duels']['bridge_four_losses'] + data['player']['stats']['Duels']['bridge_3v3v3v3_losses']
            networkLevel = (math.sqrt((2 * data['player']['networkExp']) + 30625) / 50) - 2.5
            ws = data['player']['stats']['Duels']['current_bridge_winstreak']
            if wins < 50:
                prestigecolor = Fore.YELLOW
            elif wins < 100:
                prestigecolor = Fore.LIGHTBLACK_EX
            elif wins < 200:
                prestigecolor = Fore.RESET
            elif wins < 500:
                prestigecolor = Fore.YELLOW
            elif wins < 1000:
                prestigecolor = Fore.BLUE
            elif wins < 2000:
                prestigecolor = Fore.GREEN
            elif wins < 5000:
                prestigecolor = Fore.RED
            elif wins < 10000:
                prestigecolor = Fore.LIGHTYELLOW_EX
            else:
                prestigecolor = Fore.MAGENTA
            
            if wins < criticalWins or networkLevel < criticalNWLVL:
                print(f'{Fore.RED}-------------------CRITICAL---------------------{Fore.RED}')
                print(f' {name} | {wlr} | {prestigecolor}{wins} {Fore.RESET}| {networkLevel} | {ws}')
                print(f'{Fore.RED}-------------------CRITICAL---------------------{Fore.RED}')
            elif wins < warningWins or networkLevel < warningNWLVL:
                print(f'{Fore.YELLOW}-------------------WARNING---------------------{Fore.YELLOW}')
                print(f' {name} | {wlr} | {prestigecolor}{wins} {Fore.RESET}| {networkLevel} | {ws}')
                print(f'{Fore.YELLOW}-------------------WARNING---------------------{Fore.YELLOW}')
            else:
                print(f' {name} | {wlr} | {prestigecolor}{wins} {Fore.RESET}| {networkLevel} | {ws}')


def readFile(thefile):
    thefile.seek(0,2)
    while True:
            line = thefile.readline()
            if not line:
                time.sleep(0.1)
            elif ("[Client thread/INFO]: [CHAT]", "has joined") in line:
                player = line[41:].split(' ')[0]
                getStats(player)
            elif "[Client thread/INFO]: [CHAT] Your new API key is" in line:
                recieve_api_key(line[61:])
            elif ("[Client thread/INFO]: [CHAT]", "Sending you to") in line:
                if 'windows' in platform.system.lower():
                    system('cls')
                printTable()
            
def printTable():
    title = f'''
        {Fore.CYAN}┌────────────────────────────────────────────────────────────┐
        {Fore.CYAN}│  {Fore.RESET}███╗   ██╗ ██████╗ {Fore.BLUE}███████╗███╗   ██╗██╗██████╗ ███████╗  {Fore.CYAN}│
        {Fore.CYAN}│  {Fore.RESET}████╗  ██║██╔═══██║{Fore.BLUE}██╔════╝████╗  ██║██║██╔══██╗██╔════╝  {Fore.CYAN}│
        {Fore.CYAN}│  {Fore.RESET}██╔██╗ ██║██║   ██║{Fore.BLUE}███████╗██╔██╗ ██║██║██████╔╝█████╗    {Fore.CYAN}│
        {Fore.CYAN}│  {Fore.RESET}██║╚██╗██║██║   ██║{Fore.BLUE}╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝    {Fore.CYAN}│
        {Fore.CYAN}│  {Fore.RESET}██║ ╚████║╚██████╔╝{Fore.BLUE}███████║██║ ╚████║██║██║     ███████╗  {Fore.CYAN}│
        {Fore.CYAN}│  {Fore.RESET}╚═╝  ╚═══╝ ╚═════╝ {Fore.BLUE}╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝  {Fore.CYAN}│
        {Fore.CYAN}└────────────────────────────────────────────────────────────┘
                                                            Overlay
        
            IGN    | WLR | Wins | NW LVL | WS
        '''
    print(title)

def printTitle():
    title = f'''
        {Fore.CYAN}┌────────────────────────────────────────────────────────────┐
        {Fore.CYAN}│  {Fore.RESET}███╗   ██╗ ██████╗ {Fore.BLUE}███████╗███╗   ██╗██╗██████╗ ███████╗  {Fore.CYAN}│
        {Fore.CYAN}│  {Fore.RESET}████╗  ██║██╔═══██║{Fore.BLUE}██╔════╝████╗  ██║██║██╔══██╗██╔════╝  {Fore.CYAN}│
        {Fore.CYAN}│  {Fore.RESET}██╔██╗ ██║██║   ██║{Fore.BLUE}███████╗██╔██╗ ██║██║██████╔╝█████╗    {Fore.CYAN}│
        {Fore.CYAN}│  {Fore.RESET}██║╚██╗██║██║   ██║{Fore.BLUE}╚════██║██║╚██╗██║██║██╔═══╝ ██╔══╝    {Fore.CYAN}│
        {Fore.CYAN}│  {Fore.RESET}██║ ╚████║╚██████╔╝{Fore.BLUE}███████║██║ ╚████║██║██║     ███████╗  {Fore.CYAN}│
        {Fore.CYAN}│  {Fore.RESET}╚═╝  ╚═══╝ ╚═════╝ {Fore.BLUE}╚══════╝╚═╝  ╚═══╝╚═╝╚═╝     ╚══════╝  {Fore.CYAN}│
        {Fore.CYAN}└────────────────────────────────────────────────────────────┘
                                                            Overlay
        {Fore.GREEN}Developed by sweting#9238 on Discord {Fore.BLUE}| Discord:
        {Fore.GREEN}THIS OVERLAY IS 100% FREE ON GITHUB

        {Fore.RED}This overlay is closed-source to prevent circumvention. To help improve the overlay and report known cheaters/alts, please join the Discord.{Fore.RESET}
        v0.0.1[BETA]
        '''
    print(title)

def init():
    print(f'{Fore.CYAN}Welcome! I noticed this is your first time here. I\'ll as you a couple of questions regarding parameters for this overlay. Please answer in numbers.')
    CriticalWins = int(input('What is the minimum amount of wins a player should have before a critical flag is raised?'))
    WarningWins = int(input('What is the minimum amount of wins a player should have before a warning flag is raised?'))
    CriticalNWLVL = int(input('What is the minimum network level a player should be before a critical flag is raised?'))
    WarningNWLVL = int(input(f'What is the minimum network level a player should be before a warning flag is raised?{Fore.RESET}'))
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO INFO(CriticalWins, WarningWins, CriticalNWLVL, WarningNWLVL) VALUES (?, ?, ?, ?)',(CriticalWins, WarningWins, CriticalNWLVL, WarningNWLVL,))
    conn.commit()
    conn.close()
    
def getrunningclient():
    while True:
        if input('Which client would you like to connect to? l/b/v for Lunar, BLC, or Forge/Vanilla') in ['l','b','v']:
            if input == 'l':
                logfile = open(os.getenv("APPDATA")[:-16]+"/.lunarclient/offline/1.8/logs/latest.log", "r")
            elif input == 'b':
                logfile = open(os.getenv("APPDATA")[:-16]+"/.minecraft/logs/blclient/chat/latest.log", "r")
            else:
                logfile = open(os.getenv("APPDATA")[:-16]+"/.minecraft/logs/latest.log", "r")
            readFile(logfile)

if __name__ == "__main__":
    printTitle()
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    data = cursor.execute('SELECT CriticalWins FROM INFO').fetchall()
    print(data)
    if len(data) == 0:
        init()
    printTable()
    getStats('qxide')