import datetime

from discord.ext import commands
from discord.commands import slash_command
from discord import ApplicationContext, Bot, Option, Embed, option, default_permissions
from discord.ext.commands import bot_has_permissions, has_permissions

from utils.embed_logging import EmbedLogging
from utils.logs import logger
from utils.config import Config
from utils.database import Database
from utils.utils import guilds_ids

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.embed_logging = EmbedLogging(bot)

    @slash_command(name="clear", description="Clear the channel")
    @option(name="amount", type=int, description="The amount of messages to delete", min_value=1, max_value=30, required=False)
    @default_permissions(manage_messages=True)
    @has_permissions(manage_messages=True)
    @bot_has_permissions(send_messages=True, read_messages=True, manage_messages=True)
    async def clear(self, ctx: ApplicationContext, amount: int):
        await ctx.defer(ephemeral=True)

        if amount == None:
            await ctx.channel.purge(limit=30)
            amount = 30
        else:
            await ctx.channel.purge(limit=amount)

        await ctx.respond(
            embed=Embed(
                description=f"**{amount} message(s)** ha(ve)s been **deleted** :white_check_mark:", 
                color=0x40e66c,
                timestamp=datetime.datetime.utcnow()), 
            ephemeral=True)

        if not Database.check_config(ctx.guild.id):
            channel_logging = self.bot.get_channel(
                Config.get_config(ctx.guild).get("logging_channel")
            )
        else:
            channel_logging = self.bot.get_channel(
                Database.get_config(ctx.guild.id).get("logging_channel")
            )

        if channel_logging is not None:
            embed_logging = self.embed_logging.get_embed(
                data={
                    "action": "clear",
                    "author": ctx.user.id,
                    "amount": amount,
                    "channel": ctx.channel.id
                }
            )
            await channel_logging.send(embed=embed_logging)

        log = {
            "action": "clear", 
            "author": {"id": ctx.user.id, "name": ctx.user.name+"#"+ctx.user.discriminator},
            "channel": {"id": ctx.channel.id, "name": ctx.channel.name},
            "guild": {"id": ctx.guild.id, "name": ctx.guild.name}
            }

        logger.info(log)


def setup(bot):
    bot.add_cog(Clear(bot))