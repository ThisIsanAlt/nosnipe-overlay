from threading import Thread
from tkinter import *
import time
import os
from os import system
import platform
from colorama import Fore
import requests
import json
import math
import traceback, sys
import time
root = Tk()
alive = True
uuids = {}
TitleLabels = []
DataLabels = []

def toggle_title_bar():
    global OverrideRedirect
    if OverrideRedirect:
        root.overrideredirect(False)
        OverrideRedirect = False
    else:
        root.overrideredirect(True)
        OverrideRedirect = True

def on_mode_update(*args):
    mode = ModeSetting.get()
    print(mode)
    with open('config.json', 'r') as f:
        data = json.load(f)
        data['current_mode'] = mode.lower()
        with open('config.json', 'w') as f:
            json.dump(data, f)

def create_new_window():
    global ModeSetting
    settingsWindow = Toplevel(root)
    settingsWindow.wm_attributes("-topmost", True)

    ModeSetting = StringVar(settingsWindow)
    ModeSetting.set("Bridge")
    ModeSetting.trace_add('write', on_mode_update)

    RepositionToggle = Button(settingsWindow, text = "Reposition Overlay (Toggle)", command=toggle_title_bar)
    RepositionToggle.grid(column=0, row=0, padx=(10,5), pady=(10,10), columnspan=2)

    ChangeMode = Label(settingsWindow, text = "Change Mode")
    ChangeMode.grid(row=1, column=0, padx=5, pady=(10,5))

    ModeMenu = OptionMenu(settingsWindow, ModeSetting, "Bridge", "Bedwars", "UHCDuels", "Skywars")
    ModeMenu.grid(row=1, column=1, padx=5, pady=(5,10))


def init_label_duels(terminal):
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

    winslabel = Label(terminal, font=('Calibri',20), text='WINS', bg='black', fg='white', padx=20, pady=1)
    winslabel.grid(row=0, column=6, sticky=W)

def init_label_bridge(terminal):
    playerlabel = Label(terminal, font=('Calibri',20), text='PLAYER', bg='black', fg='white', padx=100, pady=1)
    playerlabel.grid(row=0, column=0, sticky=W)

    taglabel = Label(terminal, font=('Calibri',20), text='TAG', bg='black', fg='white', padx=20, pady=1)
    taglabel.grid(row=0, column=1, sticky=W)

    wslabel = Label(terminal, font=('Calibri',20), text='WS', bg='black', fg='white', padx=20, pady=1)
    wslabel.grid(row=0, column=2, sticky=W)

    wlrlabel = Label(terminal, font=('Calibri',20), text='WLR', bg='black', fg='white', padx=20, pady=1)
    wlrlabel.grid(row=0, column=3, sticky=W)

    winslabel = Label(terminal, font=('Calibri',20), text='WINS', bg='black', fg='white', padx=20, pady=1)
    winslabel.grid(row=0, column=4, sticky=W)

    cagelabel = Label(terminal, font=('Calibri',20), text='CAGE', bg='black', fg='white', padx=20, pady=1)
    cagelabel.grid(row=0, column=5, sticky=W)

def init_label_bw(terminal):
    playerlabel = Label(terminal, font=('Calibri',20), text='PLAYER', bg='black', fg='white', padx=100, pady=1)
    playerlabel.grid(row=0, column=0, sticky=W)

    taglabel = Label(terminal, font=('Calibri',20), text='TAG', bg='black', fg='white', padx=20, pady=1)
    taglabel.grid(row=0, column=1, sticky=W)

    wslabel = Label(terminal, font=('Calibri',20), text='WS', bg='black', fg='white', padx=20, pady=1)
    wslabel.grid(row=0, column=2, sticky=W)

    kdrlabel = Label(terminal, font=('Calibri',20), text='FKDR', bg='black', fg='white', padx=20, pady=1)
    kdrlabel.grid(row=0, column=3, sticky=W)

    kdrlabel = Label(terminal, font=('Calibri',20), text='FINALS', bg='black', fg='white', padx=20, pady=1)
    kdrlabel.grid(row=0, column=4, sticky=W)

    wlrlabel = Label(terminal, font=('Calibri',20), text='WLR', bg='black', fg='white', padx=20, pady=1)
    wlrlabel.grid(row=0, column=5, sticky=W)

    playerlabel = Label(terminal, font=('Calibri',20), text='WINS', bg='black', fg='white', padx=20, pady=1)
    playerlabel.grid(row=0, column=6, sticky=W)

def init_tkinter(root):
    global OverrideRedirect
    root.geometry("1000x500+50+50")
    root.attributes('-alpha', 0.8)
    root.wm_attributes("-topmost", True)
    root.resizable(False, False)
    root['background'] = '#000000'
    root.overrideredirect(True)
    OverrideRedirect = True

    Menubar = Frame(root, bd=0, highlightthickness=0, bg='#222222', height=25, width=1000)
    Menubar.grid(row=0, column=0, sticky=W)

    SettingsButton = Button(Menubar, font=('Calibri', 10), text='Settings', command=create_new_window)
    SettingsButton.grid(row=0, column=1, sticky=W, pady=1)

    QuitButton = Button(Menubar, font=('Calibri', 10), text='Quit', command=quit)
    QuitButton.grid(row=0, column=0, sticky=W, padx=(10,0), pady=1)

    # a canvas for the main area of the window
    Terminal = Frame(root, bd=0, highlightthickness=0, bg='black', height=400, width=1000)
    Terminal.grid(row=1, column=0, sticky=W, pady=1)
    
    with open('config.json', 'r') as f:
        data = json.load(f)

    if data['current_mode'] == 'bridge':
        init_label_bridge(Terminal)
    elif data['current_mode'] == 'bedwars':
        init_label_bw(Terminal)
    elif data['current_mode'] == 'uhcduels':
        init_label_duels(Terminal)
    else:
        data['current_mode'] = 'bridge'
        init_label_bw(Terminal)

def recieve_api_key(api_key):
    '''
    func to recieve and input api key into db
    '''
    
    with open('config.json', 'r') as f:
        data = json.load(f)
        data['api_key'] = api_key
        with open('config.json', 'w') as f:
            json.dump(data, f)

def get_db_info():
    '''
    func to get api key
    '''

    with open('config.json', 'r') as f:
        data = json.load(f)
        return data.get('api_key')

def get_stats(player, mode):
    global uuids
    api_key = get_db_info()

    if player not in uuids:
        try:
            uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{player}").json()['id']
        except:
            print(f'IGN {player} not found, player is most likely nicked')
            return
        uuids[player] = uuid
    else:
        uuid = uuids.get(player)
    
    if uuid[:-32] in ['1','2','3','4','5','6','7','8','9','0']:
        tag = requests.get(f"https://thisisanalt.github.io/data/basic_info.json").json()['blacklist-no'].get(uuid, 'None')

    try:
        data = requests.get(f"https://api.hypixel.net/player?key={api_key}&uuid={uuid}").json()
    except:
        print('Could not reach the Hypixel API. It may be offline or experiencing an outage.')

    if not data['success']:
        if data['cause'] == 'Key throttle':
            time.sleep(1)
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
        get_bridge_stats(data, uuid)
    elif mode == 'bedwars':
        get_bw_stats(data, uuid)
    elif mode == 'uhcduels':
        get_uhcd_stats(data, uuid)
    return
    
def get_duels_prestige_mode(wins):
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

def get_bridge_stats(data, uuid):
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
    prestige = get_duels_prestige_mode(wins)
    
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

def get_uhcd_stats(data, uuid):
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
    prestige = get_duels_prestige_mode(wins)
    
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

def get_bw_prestige(star):  # sourcery no-metrics
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

def get_bw_stats(data, uuid):
    blacklist = requests.get(f"https://thisisanalt.github.io/data/basic_info.json").json()['blacklist']
    try:
        name = data['player']['display_name'] 
    except:
        name = data['player']['playername']
    
    #start prestige search while other data is being calculated
    star = data['player']['achievements'].get('bedwars_level', 0)
    prestige =  get_bw_prestige(star)

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

def print_bridge_table():
    print('''          IGN    | Wins | WLR | NW LVL | WS | Active Cage''')

def print_duels_mode_table():
    print('''          IGN    | Wins | WLR | NW LVL | WS ''')

def print_bw_table():
    print('''          IGN    | Star | Wins | FKDR | WLR | NW LVL | WS ''')

def print_title():
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

def read_file(thefile):
    autocheck = True
    party = []
    lobby = []
    global mode
    input('Press ENTER once connected to Hypixel.')
    print(f'Autocheck {Fore.LIGHTGREEN_EX}ACTIVE{Fore.RESET}')
    thefile.seek(0,2)

    while thread2.is_alive():
        line = thefile.readline()
        if not line:
            time.sleep(0.1)

        #autocheck + blacklist logic, handle server join/leave
        if '/INFO]: [CHAT]' in line:

            if autocheck:

                #check if player join
                if ("has joined (") in line:
                    player = line.split(' ')[3]
                    lobby.append(player)

                    if player not in lobby:
                        get_stats(player, mode)

                #clear place for new table/new players when send to new server
                elif "Sending you to" in line:
                    lobby = []
                    print_title()
                    if mode == 'bridge':
                        print_bridge_table()
                    elif mode == 'bedwars':
                        print_bw_table()
                        print(f'{Fore.GREEN}Do /who to update member list!{Fore.RESET}')
                    #change this line to include other duels mode since they use same table
                    elif mode == 'uhcduels':
                        print_duels_mode_table()

                elif "Friend request from " in line:
                    get_stats(line.split(' ')[-1].strip(), mode)           

                elif "has invited you to join their party!" in line:
                    get_stats(line.split(' ')[-8].strip(), mode)

                elif ("has invited you to join" and "'" and "party!") in line:
                    get_stats(line.split(' ')[-2].strip().strip("'s"), mode)

            if ("has joined (") in line:
                player = line.split(' ')[3]
                if player not in lobby:
                    lobby.append(player)

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
                        get_stats(player, mode)
                        lobby.append(player)

            elif 'Opponent:' in line:
                opponent = line.split(' ')[-1].strip()
                if opponent not in lobby:
                    lobby.append(opponent)

            elif 'Opponents:' in line:
                opponents = line.split(',')
                for i in opponents:
                    if i not in lobby:
                        lobby.append(i[-1].strip())

            elif "Your new API key is" in line:
                api_key = line.split(' ')[8].strip()
                recieve_api_key(api_key)
                print(f'{Fore.GREEN}API key "{api_key}" recieved and logged!{Fore.RESET}')

            elif 'Can\'t find a player by the name of' in line:
                arg = line.split(' ')[11].strip(" '")

                #statcheck
                if arg.startswith("sc-"):
                    if arg.startswith("sc-b-"):
                        if mode != 'bridge':
                            print_bridge_table()
                        get_stats(arg[5:], 'bridge',)
                    elif arg.startswith("sc-uhcd-"):
                        if mode != 'bedwars':
                            print_duels_mode_table()
                        get_stats(arg[8:], 'uhcduels',)
                    elif arg.startswith("sc-bw-"):
                        if mode != 'uhcduels':
                            print_bw_table()
                        get_stats(arg[6:], 'bedwars',)
                    elif arg.startswith('sc-lobby'):
                        for i in lobby:
                            get_stats(i, mode)

                #mode swap
                elif arg.startswith("swm-"):
                    if arg.startswith("'swm-b"):
                        mode = 'bridge'
                        print(f'{Fore.GREEN}Mode swapped to bridge!{Fore.RESET}')
                    elif arg.startswith("swm-uhcd"):
                        mode = 'uhcduels'
                        print(f'{Fore.GREEN}Mode swapped to uhcd!{Fore.RESET}')
                    elif arg.startswith("swm-bw"):
                        mode = 'bedwars'
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
                /t nosnipe-help to show this message''')

if __name__ == "__main__":
    thread2 = Thread(target = init_tkinter, args=(root,))
    thread = Thread(target = read_file)
    thread2.start()
    thread.start()

    root.mainloop()