import discord

from discord.ext import commands
from discord.commands import slash_command
from discord import Embed
from discord import ApplicationContext
from discord.ext.commands import bot_has_permissions, has_permissions
from discord import Option
from discord import Member, Bot

from utils.utils import get_color
from utils.logs import logger

guilds=[809410416685219853, 803981117069852672]

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @has_permissions(kick_members=True)
    @bot_has_permissions(send_messages=True, read_messages=True, kick_members=True)
    @slash_command(name="kick", description="Kick a member of the discord", guild_ids=guilds)
    async def kick(self, ctx: ApplicationContext, user: Option(Member, description="The user to kick"), reason: Option(str, description="The reason for kicking", required=True)):
        await ctx.defer(ephemeral=True)

        embed_user = Embed(description=f"**You have been kicked from {ctx.guild.name} !**", color=0xcc0202)
        embed_user.add_field(name="Moderator", value=ctx.user.mention, inline=True)
        embed_user.add_field(name="Reason", value=reason, inline=True)
        await user.send(embed=embed_user)

        await ctx.guild.kick(user=user, reason=reason)

        await ctx.respond(
            embed=Embed(
                description=f"**{user}** has been **kicked** :white_check_mark:", 
                color=get_color([0x42ff75, 0x42ff75, 0xa9fa52])), 
            ephemeral=True)

        log = {"action": "kick", "author": {
            "id": ctx.user.id, "name": ctx.user.display_name+"#"+ctx.user.discriminator},
            "user": {"id": user.id, "name": user.display_name+"#"+user.discriminator},
            "reason": reason,
            "guild": ctx.guild.id}
        logger.info(log)

def setup(bot):
    bot.add_cog(Kick(bot))