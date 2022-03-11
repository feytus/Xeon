import discord

import datetime
from discord.ext import commands
from discord.commands import slash_command
from discord import Option
from discord import Embed
from discord import ApplicationContext, Bot
from discord.ext.commands import bot_has_permissions, has_permissions

from utils.utils import get_color
from utils.logs import logger

guilds=[809410416685219853, 803981117069852672]

class Clear(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot  

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
                color=get_color([0x42ff75, 0x42ff75, 0xa9fa52]),
                timestamp = datetime.datetime.utcnow()), 
            ephemeral=True)

        log = {
            "action": "clear", 
            "author": {"id": ctx.user.id, "name": ctx.user.display_name+"#"+ctx.user.discriminator},
            "guild": ctx.guild.id}

        logger.info(log)

def setup(bot):
    bot.add_cog(Clear(bot))