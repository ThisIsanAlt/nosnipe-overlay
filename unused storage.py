import colorama
from colorama import Fore
colorama.init()

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

def getDuelsPrestigeMode(wins):
    if wins < 50:
        return f'\033[238m{wins}{Fore.RESET}'
    elif wins < 100:
        return Fore.LIGHTBLACK_EX
    elif wins < 200:
        return Fore.RESET
    elif wins < 500:
        return f'\033[214m{wins}{Fore.RESET}'
    elif wins < 1000:
        return f'\033[26m{wins}{Fore.RESET}'
    elif wins < 2000:
        return Fore.GREEN
    elif wins < 5000:
        return Fore.RED
    elif wins < 10000:
        return Fore.LIGHTYELLOW_EX
    else:
        return Fore.MAGENTA

print(getDuelsPrestigeMode(600))