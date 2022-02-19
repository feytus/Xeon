from distutils.log import error
import discord

from discord.ext import commands
from discord.commands import slash_command
from discord import GuildSticker, Member, Option, Guild
from discord import Embed
from discord import ApplicationContext, Bot
from discord.ext.commands import bot_has_permissions, has_permissions

from utils.utils import get_color
from utils.warning import Warning
from utils.logs import logger

guilds=[809410416685219853, 803981117069852672]


class Warnings(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @slash_command(name="warnings", description="Get a list of warnings from a member of the discord", guild_ids=guilds)
    @has_permissions(manage_roles=True)
    @bot_has_permissions(send_messages=True, read_messages=True)    
    async def warnings(
        self, 
        ctx: ApplicationContext, 
        user: Option(Member, description="The user to get warning", required=True)):
        await ctx.defer(ephemeral=True)

        guild: discord.Guild = ctx.guild

        warning = Warning(self.bot)

        warning.new_member(user=user, guild=guild)

        warnings = warning.get_warnings(user=user, guild=guild)

        embed=Embed(
            title="Warnings",
            description=f"{user} has no warnings",
            color=get_color([0x42ff75, 0x42ff75, 0xa9fa52]))

        if len(warnings) > 0:
            embed.description=f"**List of all the warnings from {user}** :"
        i = 0
        for warn in warnings:
            i += 1
            author = await self.bot.fetch_user(warn['author'])
            embed.add_field(
                inline=True, 
                name=f"Warning {i}", 
                value=f"**Moderator** : {author.mention}\n**Reason** : ``{warn['reason']}``"
                )
        await ctx.respond(embed=embed, ephemeral=True)

        log = {
            "action": "warnings", 
            "author": {"id": ctx.user.id, "name": ctx.user.display_name+"#"+ctx.user.discriminator},
            "user": {"id": user.id, "name": user.display_name+"#"+user.discriminator},
            "guild": guild
            }

        logger.info(log)

def setup(bot):
    bot.add_cog(Warnings(bot))