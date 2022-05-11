import datetime

from discord import Bot, ApplicationContext, Embed
from discord.ext import commands
from discord.ext.commands import slash_command

from utils.color import Color
from utils.logs import logger

guilds = [809410416685219853, 803981117069852672]

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
    
    @slash_command(name="ping", description="Get the bots response time", guild_ids=guilds)
    async def ping(self, ctx: ApplicationContext):
        await ctx.defer(ephemeral=True)

        latency = round(self.bot.latency * 1000)
        embed = Embed(title="Ping", description=f"** Pong :ping_pong:{latency} ms**", color=Color.get_color("lite"), timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=self.bot.user.display_avatar)

        await ctx.respond(embed=embed, ephemeral=True)

        log = {
            "action": "ping",
            "author": {"id": ctx.user.id, "name": ctx.user.name+"#"+ctx.user.discriminator},
            "guild": {"id": ctx.guild.id, "name": ctx.guild.name}
            }

        logger.info(log)

def setup(bot):
    bot.add_cog(Ping(bot))