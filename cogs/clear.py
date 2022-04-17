import datetime

from discord.ext import commands
from discord.commands import slash_command
from discord import Option, TextChannel
from discord import Embed
from discord import ApplicationContext, Bot
from discord.ext.commands import bot_has_permissions, has_permissions

from utils.embed_logging import EmbedLogging
from utils.logs import logger
from utils.config import Config

guilds=[809410416685219853, 803981117069852672]

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.config = Config(bot)
        self.embed_logging = EmbedLogging(bot)

    @slash_command(name="clear", description="Clear the channel", guild_ids=guilds)
    @has_permissions(manage_messages=True)
    @bot_has_permissions(send_messages=True, read_messages=True, manage_messages=True)
    async def clear(self, ctx: ApplicationContext, amount: Option(int, description="Amount of message to delete", required=False)):
        await ctx.defer(ephemeral=True)

        if amount == None:
            await ctx.channel.purge(limit=100)
            amount = 100
        else:
            await ctx.channel.purge(limit=amount)

        await ctx.respond(
            embed=Embed(
                description=f"**{amount} message(s)** ha(ve)s been **deleted** :white_check_mark:", 
                color=0x40e66c,
                timestamp=datetime.datetime.utcnow()), 
            ephemeral=True)

        channel_logging = await self.bot.fetch_channel(
            self.config.get_config(ctx.guild).get("logging_channel")
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
            "author": {"id": ctx.user.id, "name": ctx.user.display_name+"#"+ctx.user.discriminator},
            "channel": {"id": ctx.channel.id, "name": ctx.channel.name},
            "guild": {"id": ctx.guild.id, "name": ctx.guild.name}}

        logger.info(log)

def setup(bot):
    bot.add_cog(Clear(bot))