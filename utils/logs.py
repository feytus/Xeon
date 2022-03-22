import logging
import os
import datetime
import sys
import coloredlogs

full_date = datetime.datetime.now()
date = full_date.strftime('%Y-%m-%d-%H-%M-%S')

if "logs" not in os.listdir("."): 
    os.mkdir('logs')

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(filename=f"logs/{date}.log", encoding='utf-8', mode='w')
file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s: %(message)s')
console_handler.setLevel(logging.INFO)

logger.handlers = [file_handler, console_handler]