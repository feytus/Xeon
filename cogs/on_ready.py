from datetime import datetime
from discord.ext import commands
from discord import Game, Member, Embed
from discord import Bot, Status

from utils.utils import get_color
from utils.logs import logger


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

        activity = Game(name="https://github.com/feytus/Xeon", type=3)
        await self.bot.change_presence(status=Status.online, activity=activity)
        
        log = {"on_ready": "bot is ready"}
        logger.info(log)


def setup(bot):
    bot.add_cog(On_ready(bot))
