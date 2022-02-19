import logging
import os
import datetime

full_date = datetime.datetime.now()
date = full_date.strftime('%Y-%m-%d-%H-%M-%S')

if "logs" not in os.listdir("."): 
    os.mkdir('logs')


logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

handler = logging.FileHandler(filename=f"logs/{date}.log", encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


