import time, os
from os import system
import platform
from colorama import Fore
import requests
import sqlite3
import math
from asyncio import sleep, get_event_loop
'TABLE INFO(APIKey, CriticalWins, WarningWins, CriticalNWLVL, WarningNWLVL)'

loop = get_event_loop()
client = ''
uuids = {}
system("color")

async def recieve_api_key(api_key):
    '''
    func to recieve and input api key into db
    '''
    conn = sqlite3.connect('./lib/database.db')
    c = conn.cursor()
    try:
        c.execute(f'UPDATE INFO SET APIKey = ?', (api_key,))
    except Exception:
        c.execute(f'INSERT INTO INFO(APIKey) VALUES (?)', (api_key,))
    finally:
        conn.commit()
        print('API key recieved!')
        conn.close()

def getDBInfo():
        conn = sqlite3.connect('./lib/database.db')
        c = conn.cursor()
        data = c.execute('SELECT * FROM INFO')
        data = data.fetchone()
        conn.close()
        try:
            return data
        except:
            return

async def getStats(player, mode):
    global uuids
    api_key = getDBInfo()[0]

    if player not in uuids:
        try:
            uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player}").json()['id']
        except:
            print(f'IGN {player} not found, player is most likely nicked')
            return
        uuids[player] = uuid
    else:
        uuid = uuids.get(player)
    
    try:
        data = requests.get(f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}").json()
    except:
        print('Could not reach the Hypixel API. It may be offline or experiencing an outage.')

    if not data['success']:
        if data['cause'] == 'Key throttle':
            await sleep(1)
            data = requests.get(f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}").json()
            if not data['success']:
                print(f'Ratelimited, abandoning attempt for player {player}')
                return
        else:    
            print(data['cause'])
            return
    if mode == 'bridge':
        await getBridgeStats(data, uuid)
    elif mode == 'bw':
        await getBWStats(data, uuid)
    elif mode == 'uhcd':
        await getUHCDStats(data, uuid)

async def getBlacklist(player):
    if requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player}").json()['id'] in blacklist:
        print(f'''        {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}
                                            Player {player} is blacklisted.
        {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}''')
    
async def getDuelsPrestigeMode(wins):
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
    params = getDBInfo()
    blacklist = requests.get(f"https://thisisanalt.github.io/data/basic_info.json").json()['blacklist']
    try:
        name = data['player']['display_name'] 
    except:
        name = data['player']['playername']
    wins = data['player']['stats']['Duels'].get('bridge_duel_wins', 0) + data['player']['stats']['Duels'].get('bridge_doubles_wins', 0) \
        + data['player']['stats']['Duels'].get('bridge_four_wins', 0) + data['player']['stats']['Duels'].get('bridge_2v2v2v2_wins', 0) + data['player']['stats']['Duels'].get('bridge_3v3v3v3_wins', 0)
    
    losses = data['player']['stats']['Duels'].get('bridge_duel_losses', 0) + data['player']['stats']['Duels'].get('bridge_doubles_losses', 0) \
        + data['player']['stats']['Duels'].get('bridge_four_losses', 0) + data['player']['stats']['Duels'].get('bridge_2v2v2v2_losses', 0) + data['player']['stats']['Duels'].get('bridge_3v3v3v3_losses', 0)

    try:
        wlr = wins/losses
    except ZeroDivisionError:
        wlr = wins

    networkLevel = (math.sqrt((2 * data['player']['networkExp']) + 30625) / 50) - 2.5
    ws = data['player']['stats']['Duels']['current_bridge_winstreak']
    cage = data['player']['stats']['Duels'].get('active_cage', 'cage_async default')[5:]
    prestige = await getDuelsPrestigeMode(wins)
    
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

async def getUHCDStats(data, uuid):
    params = getDBInfo()
    blacklist = requests.get(f"https://thisisanalt.github.io/data/basic_info.json").json()['blacklist']
    try:
        name = data['player']['display_name']
    except:
        name = data['player']['playername']
        
    wins = data['player']['stats']['Duels'].get('uhc_duel_wins', 0) + data['player']['stats']['Duels'].get('uhc_doubles_wins', 0) \
        + data['player']['stats']['Duels'].get('uhc_four_wins', 0)
    
    losses = data['player']['stats']['Duels'].get('uhc_duel_losses', 0) + data['player']['stats']['Duels'].get('uhc_doubles_losses', 0) \
        + data['player']['stats']['Duels'].get('uhc_four_losses', 0)

    try:
        wlr = wins/losses
    except ZeroDivisionError:
        wlr = wins

    networkLevel = (math.sqrt((2 * data['player']['networkExp']) + 30625) / 50) - 2.5
    ws = data['player']['stats']['Duels'].get('current_uhc_winstreak')
    prestige = await getDuelsPrestigeMode(wins)
    
    if uuid in blacklist:
        print(f'''        {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}
         {name} | {prestige} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws}
        {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}''')
    elif wins < params[1] or networkLevel < params[3]:
        print(f'''        {Fore.RED}---------------------CRITICAL---------------------{Fore.RESET}
         {name} | {prestige} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws}
        {Fore.RED}---------------------CRITICAL---------------------{Fore.RESET}''')
    elif wins < params[2] or networkLevel < params[4]:
        print(f'''        {Fore.YELLOW}---------------------WARNING---------------------{Fore.RESET}
         {name} | {prestige} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws}
        {Fore.YELLOW}---------------------WARNING---------------------{Fore.RESET}''')
    else:
        print(f'         {name} | {prestige} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws}')

async def getBWPrestige(star):  # sourcery no-metrics
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
    else:
        return star

async def getBWStats(data, uuid):
    params = getDBInfo()
    blacklist = requests.get(f"https://thisisanalt.github.io/data/basic_info.json").json()['blacklist']
    try:
        name = data['player']['display_name'] 
    except:
        name = data['player']['playername']
    
    #start prestige search while other data is being calculated
    star = data['player']['achievements']['bedwars_level']
    prestige =  await getBWPrestige(star)

    wins = data['player']['stats']['Bedwars'].get('eight_one_wins_bedwars', 0) + data['player']['stats']['Bedwars'].get('eight_two_wins_bedwars', 0) \
        + data['player']['stats']['Bedwars'].get('four_three_wins_bedwars', 0)  + data['player']['stats']['Bedwars'].get('four_four_wins_bedwars', 0)

    losses = data['player']['stats']['Bedwars'].get('eight_one_losses_bedwars', 0) + data['player']['stats']['Bedwars'].get('eight_two_losses_bedwars', 0) \
        + data['player']['stats']['Bedwars'].get('four_three_losses_bedwars', 0)  + data['player']['stats']['Bedwars'].get('four_four_losses_bedwars', 0)

    try:
        wlr = wins/losses
    except ZeroDivisionError:
        wlr = wins
          
    networkLevel = (math.sqrt((2 * data['player']['networkExp']) + 30625) / 50) - 2.5
    ws = data['player']['stats']['Bedwars']['winstreak']
    
    if uuid in blacklist:
        print(f'''      {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}
         {name} | ☆{prestige} | {wins} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} 
        {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}''')
    elif wins < params[1] or networkLevel < params[3]:
        print(f'''      {Fore.RED}---------------------CRITICAL---------------------{Fore.RESET}
         {name} | ☆{prestige} | {wins} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} 
        {Fore.RED}---------------------CRITICAL---------------------{Fore.RESET}''')
    elif wins < params[2] or networkLevel < params[4]:
        print(f'''      {Fore.YELLOW}---------------------WARNING---------------------{Fore.RESET}
         {name} | ☆{prestige} | {wins} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} 
        {Fore.YELLOW}---------------------WARNING---------------------{Fore.RESET}''')
    else:
        print(f'         {name} | {prestige} | {wins} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} ')

async def printBridgeTable():
    title = f'''
        IGN    | Wins | WLR | NW LVL | WS | Active Cage
        '''
    print(title)

async def printDuelsModeTable():
    title = f'''
        IGN    | Wins | WLR | NW LVL | WS 
        '''
    print(title)

async def printBWTable():
    title = f'''
        IGN    |  ☆  | Wins | WLR | NW LVL | WS 
        '''
    print(title)

def printTitle():
    if 'windows' in platform.system().lower():
        system('cls')
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

async def readFile(thefile):  # sourcery no-metrics skip: remove-redundant-if
    autocheck = True
    hypixel = True
    global mode
    input('Press ENTER once connected to Hypixel.')
    print(f'Autocheck {Fore.LIGHTGREEN_EX}ACTIVE{Fore.RESET}')
    thefile.seek(0,2)

    while True:
        line = thefile.readline()
        if not line:
            await sleep(0.1)

        #autocheck + blacklist logic, handle server join/leave
        if hypixel:

            #check if player join
            if (f"/INFO]: [CHAT]" and "has joined") in line:
                player = line.split(' ')[3]

                try:
                    if requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player}").json()['id'] == '6654f4f13302483fa4a15e957d489ce9':
                        print('lol no you think youd get to use this to dodge shitters? fuck you lmfao')
                        input('Press ENTER to quit.')
                        break
                except:
                    pass

                if autocheck:
                    await getStats(player, mode)
                else:
                    await getBlacklist(player)

            #clear place for new table/new players when send to new server
            if ((f"/INFO]: [CHAT] Sending you to") in line) and autocheck:
                printTitle()
                if mode == 'bridge':
                    await printBridgeTable()
                elif mode == 'bw':
                    await printBWTable()
                    print(f'{Fore.GREEN}Do /who to update member list!{Fore.RESET}')
                #change this line to include other duels mode since they use same table
                elif mode == 'uhcd':
                    await printDuelsModeTable()

            if '/INFO]: [CHAT] ONLINE:' in line:
                printTitle()
                await printBWTable()
                players = line[40:-1].split(',') if client == 'l' else line[48:-1].split(',')
                for player in players:
                    await getStats(player, mode)
                    await sleep(.5)

            #log API key
            if f"/INFO]: [CHAT] Your new API key is" in line:
                api_key = line.split(' ')[8][:-1]
                await recieve_api_key(api_key)
                print(f'API key "{api_key}" recieved and logged!')

            #handle connect to anything but hypixel
            if (
                f"/INFO]: Connecting to" in line
                and 'hypixel' not in line
            ):
                print(f'Autocheck {Fore.LIGHTRED_EX}INACTIVE{Fore.RESET}')
                hypixel = False

        elif (f"/INFO]: Connecting to" in line) and ("hypixel" in line):
            if autocheck:
                print(f'Autocheck {Fore.LIGHTGREEN_EX}ACTIVE{Fore.RESET}')
            hypixel = True

        #commands logic, possible move into hypixel clause?
        if f'/INFO]: [CHAT] Can\'t find a player by the name of' in line:
            arg = line.split(' ')[11]
            print(arg)

            #statcheck
            if arg.startswith("'sc-"):
                if arg.startswith("'sc-b-"):
                    await printBridgeTable()
                    await getStats(arg[6:-2], 'bridge',)
                elif arg.startswith("'sc-uhcd-"):
                    await printDuelsModeTable()
                    await getStats(arg[9:-2], 'uhcd',)
                elif arg.startswith("'sc-bw-"):
                    await printBWTable()
                    await getStats(arg[7:-2], 'bw',)

            #mode swap
            if arg.startswith("'swm-"):
                if arg.startswith("'swm-b'"):
                   mode = 'bridge'
                   print(f'{Fore.GREEN}Mode swapped to bridge!{Fore.RESET}')
                elif arg.startswith("'swm-uhcd'"):
                    mode = 'uhcd'
                    print(f'{Fore.GREEN}Mode swapped to uhcd!{Fore.RESET}')
                elif arg.startswith("'swm-bw'"):
                    mode = 'bw'
                    print(f'{Fore.GREEN}Mode swapped to bw!{Fore.RESET}')
                else:
                    print(f'{Fore.RED}Invalid mode!{Fore.RESET}')

            #autocheck
            if arg.startswith("'ac-off'"):
                autocheck = False
                print(f'Autocheck {Fore.RED}INACTIVE{Fore.RESET}')
            elif arg.startswith("'ac-on'"):
                autocheck = True
                print(f'Autocheck {Fore.GREEN}ACTIVE{Fore.RESET}')

        #disappear when game starts, unused - fix
        if f'/INFO]: [CHAT]' and ('The Bridge Duel' or 'The Bridge Doubles' or 'The Bridge Teams') in line:
            #disappear
            pass
        
def init():
    '''
    initialize DB on generation
    '''
    print(f'{Fore.CYAN}Welcome! I noticed this is your first time here. I\'ll as you a couple of questions regarding parameters for this overlay. Please answer using digits 0-9.{Fore.RESET}')
    while True:
        try:
            CriticalWins = int(input('What is the minimum amount of wins a player should have before a critical flag is raised? '))
            WarningWins = int(input('What is the minimum amount of wins a player should have before a warning flag is raised? '))
            CriticalNWLVL = int(input('What is the minimum network level a player should be before a critical flag is raised? '))
            WarningNWLVL = int(input(f'What is the minimum network level a player should be before a warning flag is raised? '))
        except:
            print('Try again: Your answers should be in numbers using digits 0-9.')
            continue
        if (100 >= WarningWins > CriticalWins) and (50 >= WarningNWLVL > CriticalNWLVL):
            break
        print('Try again: Critical flag criteria should be lower than warning flag criteria and warning wins and network level should be below 100 and 50 respectively.')
    api_key = input('To run, this application requires your API key. You can enter that now, or press ENTER and run /api new in-game to generate a new API key. ')
    conn = sqlite3.connect('./lib/database.db')
    c = conn.cursor()
    if api_key == '':
        c.execute('INSERT INTO INFO(CriticalWins, WarningWins, CriticalNWLVL, WarningNWLVL) VALUES (?, ?, ?, ?)',(CriticalWins, WarningWins, CriticalNWLVL, WarningNWLVL,))
    else:
        c.execute('INSERT INTO INFO(CriticalWins, WarningWins, CriticalNWLVL, WarningNWLVL, APIKey) VALUES (?, ?, ?, ?, ?)',(CriticalWins, WarningWins, CriticalNWLVL, WarningNWLVL, api_key,))
    conn.commit()
    
def getrunningclient():
    global client
    '''
    get a game dir to connect to
    '''
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

if __name__ == "__main__":
    version = "0.0.2[ALPHA]"

    #print title and shit
    printTitle()
    print(f'''
            {Fore.GREEN}Developed by sweting#9238 on Discord {Fore.BLUE}| Discord:
            {Fore.GREEN}THIS OVERLAY IS AVAILABLE ON GITHUB

            {Fore.RED}This overlay is closed-source to prevent circumvention. To help improve the overlay and report known 
            cheaters/alts, please join the Discord.

            https://discord.gg/HsqHkzp2pj{Fore.RESET}
            {version}

            Commands:
                /t sc-[mode]-[player] to manually check stats
                /t swm-[bridge/bw/uhcd] to switch modes
                /t ac-[on/off] to turn autocheck on or off
        ''')
    
    #get blacklist, possibly move this into getstats for live blacklist update?
    meta = requests.get(f"https://thisisanalt.github.io/data/basic_info.json").json()
    blacklist = meta['blacklist']
    print(meta['version-messages'].get("all", ''))
    print(meta['version-messages'].get(version, ''))

    #check if version outdated and if version blacklisted
    if meta['version'] != version:
        input('You are not on the latest version! Get the latest version at https://thisisanalt.github.io/nosnipe.html \nPress enter to continue.')
    if version in meta['version-blacklist']:
        input(f'{Fore.YELLOW} This version is blacklisted and cannot be used. Please update to the latest version at https://thisisanalt.github.io/nosnipe.html\n\
        Press ENTER to quit.')
        quit()
    
    #see if database needs to be initialized
    conn = sqlite3.connect('./lib/database.db')
    c = conn.cursor()
    try:
        if len(c.execute('SELECT CriticalWins FROM INFO').fetchall()) == 0:
            init()
    except:
        c.execute('CREATE TABLE INFO(APIKey, CriticalWins, WarningWins, CriticalNWLVL, WarningNWLVL)')
        init()
    
    #get mode and run
    while True:
        mode = input('''Supported modes: 
    - "bridge"
    - "bw" 
    - "uhcd"
Select which mode to display stats from: ''')
        if mode not in ['bridge', 'bw', 'uhcd']:
            print('Try again: Please use one of our supported modes')
            continue
        break
    params = c.execute('SELECT * FROM INFO').fetchone()
    conn.close()
    loop.run_until_complete(readFile(getrunningclient()))
