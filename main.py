import time, os
from os import system
import platform
from colorama import Fore
import requests
import sqlite3
import math
import asyncio
'TABLE INFO(APIKey, CriticalWins, WarningWins, CriticalNWLVL, WarningNWLVL)'

uuids = {}
loop = asyncio.get_event_loop()
system("color")

def recieve_api_key(api_key):
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

def get_api_key():
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        data = c.execute('SELECT APIKey FROM INFO')
        data = data.fetchone()
        conn.close()
        try:
            return data[0]
        except:
            return

async def getStats(player):
    global uuids
    global mode
    api_key = get_api_key()

    if player not in uuids:
        try:
            uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player}").json()['id']
        except:
            print(f'IGN {player} not found, player is most likely nicked')
            return
        uuids[player] = uuid
    else:
        uuid = uuids.get(player)
    data = requests.get(f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}").json()

    if not data['success']:
        print(data['cause'])
        return
    elif mode == 'bridge':
        await getBridgeStats(data, uuid)
    elif mode == 'bw':
        await getBWStats(data, uuid)
    
def getDuelsPrestigeMode(wins):
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

async def getBridgeStats(data, uuid):
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
    prestige = getDuelsPrestigeMode(wins)
    
    if uuid in blacklist:
        print(f'''        {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}
         {name} | {prestige} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} | {cage}
        {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}''')
    elif wins < params[1] or networkLevel < params[3]:
        print(f'''        {Fore.RED}---------------------CRITICAL---------------------{Fore.RESET}
         {name} | {prestige} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} | {cage}
        {Fore.RED}---------------------CRITICAL---------------------{Fore.RESET}''')
    elif wins < params[2] or networkLevel < params[4]:
        print(f'''        {Fore.YELLOW}---------------------WARNING---------------------{Fore.RESET}
         {name} | {prestige} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} | {cage}
        {Fore.YELLOW}---------------------WARNING---------------------{Fore.RESET}''')
    else:
        print(f'         {name} | {prestige} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} | {cage}')

def getBWPrestige(star):
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

async def getBWStats(data, uuid):
    global params
    global blacklist
    try:
        name = data['player']['display_name'] 
    except:
        name = data['player']['playername']
    
    #start prestige search while other data is being calculated
    star = data['player']['achievements']['bedwars_level']
    prestige = getBWPrestige(star)

    wins = data['player']['stats']['Bedwars'].get('eight_one_wins_bedwars', 0) + data['player']['stats']['Bedwars'].get('eight_two_wins_bedwars', 0) \
        + data['player']['stats']['Bedwars'].get('four_three_wins_bedwars', 0)  + data['player']['stats']['Bedwars'].get('four_four_wins_bedwars', 0)

    losses = data['player']['stats']['Bedwars'].get('eight_one_losses_bedwars', 0) + data['player']['stats']['Bedwars'].get('eight_two_losses_bedwars', 0) \
        + data['player']['stats']['Bedwars'].get('four_three_losses_bedwars', 0)  + data['player']['stats']['Bedwars'].get('four_four_losses_bedwars', 0)

    wlr = wins/losses    
    networkLevel = (math.sqrt((2 * data['player']['networkExp']) + 30625) / 50) - 2.5
    ws = data['player']['stats']['Bedwars']['winstreak']
    
    if uuid in blacklist:
        print(f'''      {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}
         {name} | {prestige} | {wins} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} 
        {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}''')
    elif wins < params[1] or networkLevel < params[3]:
        print(f'''      {Fore.RED}---------------------CRITICAL---------------------{Fore.RESET}
         {name} | {prestige} | {wins} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} 
        {Fore.RED}---------------------CRITICAL---------------------{Fore.RESET}''')
    elif wins < params[2] or networkLevel < params[4]:
        print(f'''      {Fore.YELLOW}---------------------WARNING---------------------{Fore.RESET}
         {name} | {prestige} | {wins} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} 
        {Fore.YELLOW}---------------------WARNING---------------------{Fore.RESET}''')
    else:
        print(f'         {name} | {prestige} | {wins} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} ')

async def printBridgeTable():
    printTitle()
    title = f'''
        IGN    | Wins | WLR | NW LVL | WS | Active Cage
        '''
    print(title)

async def printBWTable():
    printTitle()
    title = f'''
        IGN    |  ☆  | Wins | WLR | NW LVL | WS 
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
                                                            Overlay by sweting{Fore.RESET}'''
    print(title)

async def readFile(thefile):
    autocheck = True
    input('Press ENTER once connected to Hypixel.')
    print(f'Autocheck {Fore.LIGHTGREEN_EX}ACTIVE{Fore.RESET}')
    thefile.seek(0,2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
        if autocheck:
            if ("[Client thread/INFO]: [CHAT]" and "has joined") in line:
                player = line[40:].split(' ')[0]
                await getStats(player)
            elif "[Client thread/INFO]: [CHAT] Your new API key is" in line:
                recieve_api_key(line[61:])
            elif ("[Client thread/INFO]: [CHAT] Sending you to") in line:
                if 'windows' in platform.system().lower():
                    system('cls')
                if mode == 'bridge':
                    await printBridgeTable()
                elif mode == 'bw':
                    await printBWTable()
        elif ("[Client thread/INFO]: [CHAT] Connecting to") in line:
            if "hypixel" not in line:
                print(f'Autocheck {Fore.LIGHTRED_EX}INACTIVE{Fore.RESET}')
            else:
                print(f'Autocheck {Fore.LIGHTGREEN_EX}ACTIVE{Fore.RESET}')
        
def init():
    print(f'{Fore.CYAN}Welcome! I noticed this is your first time here. I\'ll as you a couple of questions regarding parameters for this overlay. Please answer using digits 0-9.{Fore.RESET}')
    while True:
        try:
            CriticalWins = int(input('What is the minimum amount of wins a player should have before a critical flag is raised? '))
            WarningWins = int(input('What is the minimum amount of wins a player should have before a warning flag is raised? '))
            CriticalNWLVL = int(input('What is the minimum network level a player should be before a critical flag is raised? '))
            WarningNWLVL = int(input(f'What is the minimum network level a player should be before a warning flag is raised?'))
        except:
            print('Try again: Your answers should be in numbers using digits 0-9.')
            continue
        if (100 >= CriticalWins > WarningWins) and (50 >= CriticalNWLVL > WarningNWLVL):
            break
        print('Try again: Critical flag criteria should be lower than warning flag criteria and warning wins and network level should be below 100 and 50 respectively.')
    api_key = input('To run, this application requires your API key. You can enter that now, or press ENTER and run /api new in-game to generate a new API key.')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    if api_key == '':
        c.execute('INSERT INTO INFO(CriticalWins, WarningWins, CriticalNWLVL, WarningNWLVL) VALUES (?, ?, ?, ?)',(CriticalWins, WarningWins, CriticalNWLVL, WarningNWLVL,))
    else:
        c.execute('INSERT INTO INFO(CriticalWins, WarningWins, CriticalNWLVL, WarningNWLVL, APIKey) VALUES (?, ?, ?, ?, ?)',(CriticalWins, WarningWins, CriticalNWLVL, WarningNWLVL, api_key,))
    conn.commit()
    
def getrunningclient():
    while True:
        client = str(input('''Which client would you like to connect to?
    l - Lunar Client
    b - Badlion Client
    v - Vanilla/Forge OR default log location
    Other clients may not be supported.'''))
        if client == 'l':
            logfile = open(os.getenv("APPDATA")[:-16]+"/.lunarclient/offline/1.8/logs/latest.log", "r")
        elif client == 'b':
            logfile = open(os.getenv("APPDATA")+"/.minecraft/logs/blclient/chat/latest.log", "r")
        elif client == 'v':
            logfile = open(os.getenv("APPDATA")+"/.minecraft/logs/latest.log", "r")
        else:
            print('Try again: Your answer should be a single character and be either "l", "b", or "v".')
            continue
        return logfile

def validateToken(token):
    pass

if __name__ == "__main__":
    version = "0.0.2[ALPHA]"
    printTitle()
    f'''
            {Fore.GREEN}Developed by sweting#9238 on Discord {Fore.BLUE}| Discord:
            {Fore.GREEN}THIS OVERLAY IS AVAILABLE ON GITHUB

            {Fore.RED}This overlay is closed-source to prevent circumvention. To help improve the overlay and report known cheaters/alts, please join the Discord.{Fore.RESET}
            {version}
        '''
    meta = requests.get(f"https://thisisanalt.github.io/data/basic_info.json").json()
    blacklist = meta['blacklist']
    if meta['version'] != version:
        input('You are not on the latest version! Get the latest version at https://thisisanalt.github.io/nosnipe.html \nPress enter to continue.')
    if version in meta['version-blacklist']:
        input(f'{Fore.YELLOW} This version is blacklisted and cannot be used. Please update to the latest version at https://thisisanalt.github.io/nosnipe.html')
        quit()     
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    try:
        if len(c.execute('SELECT CriticalWins FROM INFO').fetchall()) == 0:
            init()
    except:
        c.execute('CREATE TABLE INFO(APIKey, CriticalWins, WarningWins, CriticalNWLVL, WarningNWLVL)')
        init()
    while True:
        mode = input('''Supported modes: 
    - "bridge"
    - "bw" 
Select which mode to display stats from: ''')
        if mode not in ['bridge', 'bw']:
            print('Try again: Please use either "bridge" or "bw"')
            continue
        break
    params = c.execute('SELECT * FROM INFO').fetchone()
    conn.close()
    loop.run_until_complete(readFile(getrunningclient()))
