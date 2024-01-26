import asyncio
import configparser
import os
import subprocess
import time
from multiprocessing import Process

from telegram.telegram_bot import BotHandlers
num_processes = os.cpu_count()

def start_bot():
    token = '6928876462:AAEaBttMIEhZhi4Hh7U1GKDVFL2693wNpvY'
    bot = BotHandlers(token=token)
    asyncio.run(bot.handlers())

def start_web():
    os.system("cd ..")
    os.system("venv/scripts/activate")
    os.system("cd webForm")
    os.system("python manage.py runserver")

    # subprocess.run('cd .. ; venv/scripts/activate ; cd webForm ; python manage.py', shell=True)


if __name__ == "__main__":

    p1 = Process(target=start_bot, args=())
    # p2 = Process(target=start_web, args=())

    p1.start()
    # p2.start()

    # p1.join()
    # p2.join()


