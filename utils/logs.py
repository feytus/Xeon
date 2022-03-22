import logging
import os
import datetime
import sys

from colorama import Fore
from logging import LogRecord


full_date = datetime.datetime.now()
date = full_date.strftime('%Y-%m-%d-%H-%M-%S')

if "logs" not in os.listdir("."): 
    os.mkdir('logs')


fmt = '%(asctime)s:%(name)s:{}%(levelname)s: %(message)s{}'

FORMATS = {
    logging.DEBUG: fmt.format(Fore.GREEN, Fore.RESET),
    logging.INFO: fmt.format(Fore.CYAN, Fore.RESET),
    logging.ERROR: fmt.format(Fore.RED, Fore.RESET),
    logging.WARNING: fmt.format(Fore.YELLOW, Fore.RESET),
    logging.CRITICAL: fmt.format(Fore.MAGENTA, Fore.RESET),
}

class CustomFormatter(logging.Formatter):
    def format(self, record: LogRecord) -> str:
        log_fmt = FORMATS[record.levelno]
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(filename=f"logs/{date}.log", encoding='utf-8', mode='w')
file_handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(CustomFormatter(), style="%(")
console_handler.setLevel(logging.INFO)

logger.handlers = [file_handler, console_handler]