from discord.ext import commands
from discord import Embed
from discord import ApplicationContext, Bot

from utils.utils import get_color
from utils.logs import logger

import time

class On_ready(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.xeon = """
██╗  ██╗███████╗ █████╗ ███╗  ██╗
╚██╗██╔╝██╔════╝██╔══██╗████╗ ██║
╚███╔╝ █████╗  ██║  ██║██╔██╗██║
██╔██╗ ██╔══╝  ██║  ██║██║╚████║
██╔╝╚██╗███████╗╚█████╔╝██║ ╚███║
╚═╝  ╚═╝╚══════╝ ╚════╝ ╚═╝  ╚══╝
"""

    @commands.Cog.listener()
    async def on_ready(self):  
        print(self.xeon)
        print("latency :", round(self.bot.latency * 1000), "ms")
        log = {"on_ready": "bot is ready"}
        logger.info(log)
            
def setup(bot):
    bot.add_cog(On_ready(bot))