import os
from os import system
import platform
from colorama import Fore
import requests
import json
import math
from asyncio import sleep, get_event_loop
'TABLE INFO(APIKey, CriticalWins, WarningWins, CriticalNWLVL, WarningNWLVL)'

loop = get_event_loop()
client = ''
uuids = {}

async def recieve_api_key(api_key):
    '''
    func to recieve and input api key into db
    '''
    
    with open('config.json', 'r') as f:
        data = json.load(f)
        data['api_key'] = api_key
        with open('config.json', 'w') as f:
            json.dump(data, f)

def getDBInfo():
    '''
    func to get api key
    '''

    with open('config.json', 'r') as f:
        data = json.load(f)
        return data.get('api_key')

async def getStats(player, mode):
    global uuids
    api_key = getDBInfo()

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
        elif data['cause'] == 'Invalid API key':
            print('API key invalid! Run "/api new" to generate a new one!')
        else:    
            print(data['cause'])
    elif data["player"] == 'null':
        print(f'IGN {player} not found, player is most likely nicked')
    elif mode == 'bridge':
        await getBridgeStats(data, uuid)
    elif mode == 'bw':
        await getBWStats(data, uuid)
    elif mode == 'uhcd':
        await getUHCDStats(data, uuid)
    return

async def getBlacklist(player):
    try:
        if requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player}").json()['id'] in blacklist:
            print(f'''        {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}
                                                Player {player} is blacklisted.
            {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}''')
        else:
            print(f'        [INACTIVE AUTOCHECK] Player {player} has joined.')
    except:
        print(f'IGN {player} not found, player is most likely nicked')
    
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
    cage = data['player']['stats']['Duels'].get('active_cage', 'cage_default')[5:]
    prestige = await getDuelsPrestigeMode(wins)
    
    if uuid in blacklist:
        print(f'''          {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}
         {name} | {prestige} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} | {cage}
        {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}''')
    elif wins < 50 or networkLevel < 10:
        print(f'''          {Fore.RED}---------------------CRITICAL---------------------{Fore.RESET}
         {name} | {prestige} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} | {cage}
        {Fore.RED}---------------------CRITICAL---------------------{Fore.RESET}''')
    elif wins < 100 or networkLevel < 25:
        print(f'''          {Fore.YELLOW}---------------------WARNING---------------------{Fore.RESET}
         {name} | {prestige} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} | {cage}
        {Fore.YELLOW}---------------------WARNING---------------------{Fore.RESET}''')
    else:
        print(f'         {name} | {prestige} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} | {cage}')

async def getUHCDStats(data, uuid):
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
        print(f'''          {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}
         {name} | {prestige} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws}
        {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}''')
    elif wins < 50 or networkLevel < 10:
        print(f'''          {Fore.RED}---------------------CRITICAL---------------------{Fore.RESET}
         {name} | {prestige} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws}
        {Fore.RED}---------------------CRITICAL---------------------{Fore.RESET}''')
    elif wins < 100 or networkLevel < 25:
        print(f'''          {Fore.YELLOW}---------------------WARNING---------------------{Fore.RESET}
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
    blacklist = requests.get(f"https://thisisanalt.github.io/data/basic_info.json").json()['blacklist']
    try:
        name = data['player']['display_name'] 
    except:
        name = data['player']['playername']
    
    #start prestige search while other data is being calculated
    star = data['player']['achievements'].get('bedwars_level', 0)
    prestige =  await getBWPrestige(star)

    wins = data['player']['stats']['Bedwars'].get('eight_one_wins_bedwars', 0) + data['player']['stats']['Bedwars'].get('eight_two_wins_bedwars', 0) \
        + data['player']['stats']['Bedwars'].get('four_three_wins_bedwars', 0)  + data['player']['stats']['Bedwars'].get('four_four_wins_bedwars', 0)

    losses = data['player']['stats']['Bedwars'].get('eight_one_losses_bedwars', 0) + data['player']['stats']['Bedwars'].get('eight_two_losses_bedwars', 0) \
        + data['player']['stats']['Bedwars'].get('four_three_losses_bedwars', 0)  + data['player']['stats']['Bedwars'].get('four_four_losses_bedwars', 0)
    
    fks = data['player']['stats']['Bedwars'].get('eight_one_final_kills_bedwars', 0) + data['player']['stats']['Bedwars'].get('eight_two_final_kills_bedwars', 0) \
        + data['player']['stats']['Bedwars'].get('four_three_final_kills_bedwars', 0)  + data['player']['stats']['Bedwars'].get('four_four_final_kills_bedwars', 0)
    fds = data['player']['stats']['Bedwars'].get('eight_one_final_deaths_bedwars', 0) + data['player']['stats']['Bedwars'].get('eight_two_final_deaths_bedwars', 0) \
        + data['player']['stats']['Bedwars'].get('four_three_final_deaths_bedwars', 0)  + data['player']['stats']['Bedwars'].get('four_four_final_deaths_bedwars', 0)
        
    fkdr = fks/fds

    try:
        wlr = wins/losses
    except ZeroDivisionError:
        wlr = wins
          
    networkLevel = (math.sqrt((2 * data['player']['networkExp']) + 30625) / 50) - 2.5
    ws = data['player']['stats']['Bedwars']['winstreak']
    
    if uuid in blacklist:
        print(f'''        {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}
         {name} |  {prestige}  | {wins} | {round(fkdr, 2)} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} 
        {Fore.RED}---------------------{Fore.YELLOW}BLACKLISTED{Fore.RED}---------------------{Fore.RESET}''')
    elif wins < 50 or networkLevel < 10:
        print(f'''        {Fore.RED}---------------------CRITICAL---------------------{Fore.RESET}
         {name} |  {prestige}  | {wins} | {round(fkdr, 2)} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} 
        {Fore.RED}---------------------CRITICAL---------------------{Fore.RESET}''')
    elif wins < 100 or networkLevel < 25:
        print(f'''        {Fore.YELLOW}---------------------WARNING---------------------{Fore.RESET}
         {name} |  {prestige}  | {wins} | {round(fkdr, 2)} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} 
        {Fore.YELLOW}---------------------WARNING---------------------{Fore.RESET}''')
    else:
        print(f'         {name} | ☆{prestige} | {wins} | {round(fkdr, 2)} | {round(wlr, 2)} | {round(networkLevel, 2)} | {ws} ')

async def printBridgeTable():
    print('''          IGN    | Wins | WLR | NW LVL | WS | Active Cage''')

async def printDuelsModeTable():
    print('''          IGN    | Wins | WLR | NW LVL | WS ''')

async def printBWTable():
    print('''          IGN    | Star | Wins | FKDR | WLR | NW LVL | WS ''')

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

async def readFile(thefile):  # sourcery no-metrics
    autocheck = True
    party = []
    lobby = []
    global mode
    input('Press ENTER once connected to Hypixel.')
    print(f'Autocheck {Fore.LIGHTGREEN_EX}ACTIVE{Fore.RESET}')
    thefile.seek(0,2)

    while True:
        line = thefile.readline()
        if not line:
            await sleep(0.1)

        #autocheck + blacklist logic, handle server join/leave
        if '/INFO]: [CHAT]' in line:

            if autocheck:

                #check if player join
                if ("has joined (") in line:
                    player = line.split(' ')[3]
                    lobby.append(player)

                    if player not in lobby:
                        await getStats(player, mode)

                #clear place for new table/new players when send to new server
                elif "Sending you to" in line:
                    lobby = []
                    printTitle()
                    if mode == 'bridge':
                        await printBridgeTable()
                    elif mode == 'bw':
                        await printBWTable()
                        print(f'{Fore.GREEN}Do /who to update member list!{Fore.RESET}')
                    #change this line to include other duels mode since they use same table
                    elif mode == 'uhcd':
                        await printDuelsModeTable()

                elif "Friend request from " in line:
                    await getStats(line.split(' ')[-1].strip(), mode)           

                elif "has invited you to join their party!" in line:
                    await getStats(line.split(' ')[-8].strip(), mode)        

            if ("has joined (") in line:
                player = line.split(' ')[3]
                if player not in lobby:
                    lobby.append(player)
                    await getBlacklist(player)

            elif "Sending you to" in line:
                lobby = []

            elif ("You have joined" and "party!") in line:
                split = line.split(' ')
                if split[-2].endswith("'"):
                    party.append(split[-2][:-1])
                else:
                    party.append(split[-2][:-2])

            elif ("You left the party") in line:
                party = []

            elif 'ONLINE:' in line:
                players = line[38:] if client == 'l' else line[47:]
                for player in players.split(','):
                    player = player.strip()
                    if player not in lobby:
                        await getStats(player, mode)
                        lobby.append(player)
                        await sleep(.5)

            elif 'Opponent:' in line:
                opponent = line.split(' ')[-1].strip()
                if opponent not in lobby:
                    lobby.append(opponent)

            elif 'Opponents:' in line:
                opponents = line.split(',')
                for i in opponents:
                    lobby.append(i[-1].strip())

            elif "Your new API key is" in line:
                api_key = line.split(' ')[8].strip()
                await recieve_api_key(api_key)
                print(f'{Fore.GREEN}API key "{api_key}" recieved and logged!{Fore.RESET}')

            elif 'Can\'t find a player by the name of' in line:
                arg = line.split(' ')[11].strip(" '")

                #statcheck
                if arg.startswith("sc-"):
                    if arg.startswith("sc-b-"):
                        if mode != 'bridge':
                            await printBridgeTable()
                        await getStats(arg[5:], 'bridge',)
                    elif arg.startswith("sc-uhcd-"):
                        if mode != 'bw':
                            await printDuelsModeTable()
                        await getStats(arg[8:], 'uhcd',)
                    elif arg.startswith("sc-bw-"):
                        if mode != 'uhcd':
                            await printBWTable()
                        await getStats(arg[6:], 'bw',)
                    elif arg.startswith('sc-lobby'):
                        for i in lobby:
                            await getStats(i, mode)

                #mode swap
                elif arg.startswith("swm-"):
                    if arg.startswith("'swm-b"):
                        mode = 'bridge'
                        print(f'{Fore.GREEN}Mode swapped to bridge!{Fore.RESET}')
                    elif arg.startswith("swm-uhcd"):
                        mode = 'uhcd'
                        print(f'{Fore.GREEN}Mode swapped to uhcd!{Fore.RESET}')
                    elif arg.startswith("swm-bw"):
                        mode = 'bw'
                        print(f'{Fore.GREEN}Mode swapped to bw!{Fore.RESET}')
                    else:
                        print(f'{Fore.RED}Invalid mode!{Fore.RESET}')

                #autocheck
                elif arg.startswith("ac-off"):
                    autocheck = False
                    print(f'Autocheck {Fore.RED}INACTIVE{Fore.RESET}')
                elif arg.startswith("ac-on"):
                    autocheck = True
                    print(f'Autocheck {Fore.LIGHTGREEN_EX}ACTIVE{Fore.RESET}')

                elif arg.startswith("apikey-register-"):
                    api_key = arg[7:-2]
                    recieve_api_key(api_key)
                    print(f'{Fore.GREEN}API Key "{api_key}" recieved and logged!{Fore.RESET}')

                elif arg.startswith("nosnipe-help"):
                    print('''            Commands:
                /t sc-[mode]-[player] to manually check stats
                -   /t sc-lobby to check stats of entire lobby
                /t swm-[bridge/bw/uhcd] to switch modes
                /t ac-[on/off] to turn autocheck on or off
                /t apikey-register-[apikey] to manually register API key
                /t nosnipe-quit to close the overlay
                /t nosnipe-help to show this message''')

                elif arg.startswith("nosnipe-quit"):
                    quit()
    
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
    import traceback, sys

    try:
        version = "0.3.0[ALPHA]"

        #print title and shit
        printTitle()
        print(f'''
            {Fore.GREEN}Developed by sweting#9238 on Discord {Fore.BLUE}| Discord: https://discord.gg/HsqHkzp2pj
            {Fore.GREEN}THIS OVERLAY IS 100% FREE ON GITHUB - OPEN SOURCE - https://github.com/ThisIsanAlt/nosnipe-overlay

            {Fore.RED}To help improve the overlay and report known cheaters/alts, please join the Discord.{Fore.RESET}

            {Fore.LIGHTRED_EX}THIS IS A USE-AT-OWN-RISK OVERLAY. While theoretically against Hypixel rules, no one
            has been banned for similar programs so far.{Fore.RESET}

            {version}

            Commands:
                /t sc-[mode]-[player] to manually check stats
                /t swm-[bridge/bw/uhcd] to switch modes
                /t ac-[on/off] to turn autocheck on or off
                /t nosnipe-quit to close the overlay
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
        with open('config.json', 'r') as f:
            data = json.load(f)

            if not data.get('api_key'):
                api_key = input('To run, this application requires your API key. You can enter that now, or press ENTER and run /api new in-game to generate a new API key. ')
                data['api_key'] = api_key
                with open ('config.json', 'w') as f:
                    json.dump(data, f)
        
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
        loop.run_until_complete(readFile(getrunningclient()))
    except Exception as e:
        if isinstance(e, requests.exceptions.ConnectionError):
            input('Could not connect to API. Have you checked your network?\nPress ENTER to quit.')
        else:
            print(f'{Fore.LIGHTRED_EX}EXCEPTION OCCURED:\nPlease copy the following and paste it in #bug-reports in the Discord!{Fore.YELLOW}')
            traceback.print_exception(type(e), e, e.__traceback__, file=sys.stderr)
            print(f'{Fore.GREEN}VERSION: {version}')
            input(f'{Fore.RESET}Press ENTER to quit.')
    
