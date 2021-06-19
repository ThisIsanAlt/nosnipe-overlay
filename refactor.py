import time, os
from os import system
import platform
from colorama import Fore
import requests
import sqlite3
import math
import asyncio

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
                if not "hypixel" in line:
                    print(f'Autocheck {Fore.LIGHTRED_EX}INACTIVE{Fore.RESET}')
                    autocheck = False
        elif ("[Client thread/INFO]: [CHAT] Connecting to") in line:
            if "hypixel" in line:
                print(f'Autocheck {Fore.LIGHTGREEN_EX}ACTIVE{Fore.RESET}')
                autocheck = True