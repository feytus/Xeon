import datetime

from discord.ext import commands
from discord import Embed
from discord import ApplicationContext, Bot
from utils.utils import get_color

from utils.logs import logger


class On_error(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: ApplicationContext,  error):
        await ctx.respond(embed=Embed(
            title="Error",
            description=f"**{error}**", color=get_color([0xf54531, 0xf57231, 0xf53145]),
            timestamp = datetime.datetime.utcnow()),
            ephemeral=True)

        log = {"command": ctx.command, "author": ctx.author.id, "error": error}
        logger.warning(log)


def setup(bot):
    bot.add_cog(On_error(bot))
