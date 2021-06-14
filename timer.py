import time, os
from os import system
import platform
from colorama import Fore
import requests
import sqlite3
import math
import timeit

'TABLE INFO(APIKey, CriticalWins, WarningWins, CriticalNWLVL, WarningNWLVL)'

uuids = {}

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

def getStats(player, data):
    global uuids
    global mode
    api_key = get_api_key()

    if player not in uuids:
        uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player}").json()['id']
        if not uuid:
            print(f'IGN {player} not found, player is most likely nicked')
            return
        uuids[player] = uuid
    else:
        uuid = uuids.get(player)



    if not data['success']:
        print(data['cause'])
        return
    elif mode == 'bridge':
        getBridgeStats(data, uuid)
    elif mode == 'bw':
        getBWStats(data, uuid)
    
def getDuelsPrestigeColor(wins):
    if wins < 50:
        return Fore.YELLOW
    elif wins < 100:
        return Fore.LIGHTBLACK_EX
    elif wins < 200:
        return Fore.RESET
    elif wins < 500:
        return Fore.YELLOW
    elif wins < 1000:
        return Fore.BLUE
    elif wins < 2000:
        return Fore.GREEN
    elif wins < 5000:
        return Fore.RED
    elif wins < 10000:
        return Fore.LIGHTYELLOW_EX
    else:
        return Fore.MAGENTA

def getBridgeStats(data, uuid):
    global params
    global blacklist
    try:
        name = data['player']['display_name'] 
    except:
        name = data['player']['playername']
    wins = data['player']['stats']['Duels'].get('bridge_duel_wins', 0) + data['player']['stats']['Duels'].get('bridge_doubles_wins', 0) \
        + data['player']['stats']['Duels'].get('bridge_four_wins', 0) + data['player']['stats']['Duels'].get('bridge_2v2v2v2_wins', 0) + data['player']['stats']['Duels'].get('bridge_3v3v3v3_wins', 0)
    wlr = wins/data['player']['stats']['Duels'].get('bridge_duel_losses', 0) + data['player']['stats']['Duels'].get('bridge_doubles_losses', 0) \
        + data['player']['stats']['Duels'].get('bridge_four_losses', 0) + data['player']['stats']['Duels'].get('bridge_2v2v2v2_losses', 0) + data['player']['stats']['Duels'].get('bridge_3v3v3v3_losses', 0)
    networkLevel = (math.sqrt((2 * data['player']['networkExp']) + 30625) / 50) - 2.5
    ws = data['player']['stats']['Duels']['current_bridge_winstreak']
    cage = data['player']['stats']['Duels']['active_cage'][5:]
    prestigecolor = getDuelsPrestigeColor(wins)
    
    if uuid in blacklist:
        print(f'''        {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}
         {name} | {prestigecolor}{wins} {Fore.RESET} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} | {cage}
        {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}''')
    elif wins < params[1] or networkLevel < params[3]:
        print(f'''       {Fore.RED}---------------------CRITICAL---------------------{Fore.RESET}
         {name} | {prestigecolor}{wins} {Fore.RESET} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} | {cage}
        {Fore.RED}---------------------CRITICAL---------------------{Fore.RESET}''')
    elif wins < params[2] or networkLevel < params[4]:
        print(f'''       {Fore.YELLOW}---------------------WARNING---------------------{Fore.RESET}
         {name} | {prestigecolor}{wins} {Fore.RESET} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} | {cage}
        {Fore.YELLOW}---------------------WARNING---------------------{Fore.RESET}''')
    else:
        print(f'         {name} | {prestigecolor}{wins} {Fore.RESET} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} | {cage}')

def getBWPrestige(star):
    if star < 100:
        return f'{Fore.LIGHTBLACK_EX}{star}{Fore.RESET}'
    elif star < 200 or (star < 1200 and star > 1100):
        return star
    elif star < 300 or (star < 1300 and star > 1200):
        return f'\033[214m{star}{Fore.RESET}'
    elif star < 400 or (star < 1400 and star > 1300):
        return f'\033[33m{star}{Fore.RESET}'
    elif star < 500 or (star < 1500 and star > 1400):
        return f'{Fore.GREEN}{star}{Fore.RESET}'
    elif star < 600 or (star < 1600 and star > 1500):
        return f'\033[30m{star}{Fore.RESET}'
    elif star < 700 or (star < 1700 and star > 1600):
        return f'{Fore.RED}{star}{Fore.RESET}'
    elif star < 800 or (star < 1800 and star > 1700):
        return f'\033[205m{star}{Fore.RESET}'
    elif star < 900 or (star < 1900 and star > 1800):
       return f'\033[26m{star}{Fore.RESET}'
    elif star < 1000:
        return f'{Fore.MAGENTA}{star}{Fore.RESET}'
    elif star < 1100:
        star = str(star)
        return f'\033[202m{star[0]}{Fore.YELLOW}{star[1]}{Fore.LIGHTGREEN_EX}{star[2]}\033[39m{star[3]}{Fore.RESET}'
    elif star < 2000:
        return f'{Fore.MAGENTA}{star}{Fore.RESET}'
    elif star < 2100:
        star = str(star)
        return f'{Fore.LIGHTBLACK_EX}{star[0]}{Fore.RESET}{star[1]}{star[2]}{Fore.LIGHTBLACK_EX}{Fore.RESET}'
    elif star < 2200:
        star = str(star)
        return f'{star[0]}{Fore.LIGHTYELLOW_EX}{star[1]}{star[2]}\033[172m{star[3]}{Fore.RESET}'
    elif star < 2300:
        star = str(star)
        return f'\033[172m{star[0]}{Fore.RESET}{star[1]}{star[2]}\033[33m{star[4]}{Fore.RESET}'

def getBWStats(data, uuid):
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
        print(f'''        {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}
         {name} | {prestige} | {wins} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} 
        {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}''')
    elif wins < params[1] or networkLevel < params[3]:
        print(f'''       {Fore.RED}---------------------CRITICAL---------------------{Fore.RESET}
         {name} | {prestige} | {wins} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} 
        {Fore.RED}---------------------CRITICAL---------------------{Fore.RESET}''')
    elif wins < params[2] or networkLevel < params[4]:
        print(f'''       {Fore.YELLOW}---------------------WARNING---------------------{Fore.RESET}
         {name} | {prestige} | {wins} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} 
        {Fore.YELLOW}---------------------WARNING---------------------{Fore.RESET}''')
    else:
        print(f'         {name} | {prestige} | {wins} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} ')

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
                if 'windows' in platform.system().lower():
                    system('cls')
                if mode == 'bridge':
                    printBridgeTable()
                elif mode == 'bw':
                    printBWTable()
            
def printBridgeTable():
    printTitle()
    title = f'''
            IGN    | Wins | WLR | NW LVL | WS | Active Cage
        '''
    print(title)

def printBWTable():
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

def init():
    print(f'{Fore.CYAN}Welcome! I noticed this is your first time here. I\'ll as you a couple of questions regarding parameters for this overlay. Please answer using digits 0-9.')
    while True:
        try:
            CriticalWins = int(input('What is the minimum amount of wins a player should have before a critical flag is raised? '))
            WarningWins = int(input('What is the minimum amount of wins a player should have before a warning flag is raised? '))
            CriticalNWLVL = int(input('What is the minimum network level a player should be before a critical flag is raised? '))
            WarningNWLVL = int(input(f'What is the minimum network level a player should be before a warning flag is raised? {Fore.RESET}'))
        except:
            print('Try again: Your answers should be in numbers using digits 0-9.')
            continue
        if (CriticalWins < WarningWins < 100) and (CriticalNWLVL < WarningNWLVL < 50):
            break
        print('Try again: Critical flag criteria should be lower than warning flag criteria and warning wins and network level should be below 100 and 50 respectively.')
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('INSERT INTO INFO(CriticalWins, WarningWins, CriticalNWLVL, WarningNWLVL) VALUES (?, ?, ?, ?)',(CriticalWins, WarningWins, CriticalNWLVL, WarningNWLVL,))
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
        readFile(logfile)

def validateToken(token):
    pass

if __name__ == "__main__":
    version = "0.0.1[BETA]"
    meta = requests.get(f"https://thisisanalt.github.io/data/basic_info.json").json()
    blacklist = meta['blacklist']
    mode = 'bw'
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    params = c.execute('SELECT * FROM INFO').fetchone()
    conn.close()
    times = []
    data = requests.get(f"https://api.hypixel.net/player?key={get_api_key()}&uuid=c78a19a8156e4ddfbdbab58d0696ba53").json()
    for i in range(10000):
        timestart = time.perf_counter()
        getStats('fqrs', data)
        timeend = time.perf_counter()
        walltime = timeend-timestart
        times.append(walltime)
        if i % 1000 == 0:
            print(f'HEARTBEAT: {i}')
    avg = 0.0
    for i in times:
        avg+=i
        avg/=2
    print('Average time:', avg)
    print('Last time', walltime)
        