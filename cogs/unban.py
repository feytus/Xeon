import discord

from discord.ext import commands
from discord.commands import slash_command
from discord import GuildSticker, Option, User
from discord import Embed
from discord import ApplicationContext, Bot
from discord.ext.commands import bot_has_permissions, has_permissions

from utils.utils import get_color
from utils.logs import logger

guilds=[809410416685219853, 803981117069852672]

class Unban(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot  

    @slash_command(name="unban", description="Unban a banned member", guild_ids=guilds)
    @has_permissions(ban_members=True)
    @bot_has_permissions(send_messages=True, read_messages=True, ban_members=True)
    async def unban(
        self, 
        ctx: ApplicationContext, 
        user: Option(str, description="The user to unban : exemple#1234 or the user ID", required=True), 
        reason: Option(str, description="The reaon for unbanning this user", required=False)="No reason given"):
        await ctx.defer(ephemeral=True)

        guild: discord.Guild = ctx.guild

        banned_users_list = await guild.bans()

        embed = Embed(title="Unban", description="**This user is not banned** :white_check_mark:", color=get_color([0x42c5f5, 0xf54275, 0x70fc6d]))

        log = {
            "action": "unban", 
            "author": {"id": ctx.user.id, "name": ctx.user.display_name+"#"+ctx.user.discriminator},
            "reason": reason,
            "guild": ctx.guild.id
            }

        for banned_users in banned_users_list:
            if user == str(banned_users.user.id):
                user: User = await self.bot.fetch_user(banned_users.user.id)
                await guild.unban(user, reason)
                embed.description = f"**{user.name} has been unbanned**"
                log['user']['id'] = user.id
            elif str(user) == f"{banned_users.user.name}#{banned_users.user.discriminator}":
                user: User = await self.bot.fetch_user(banned_users.user.id)
                await guild.unban(user, reason)
                embed.description = f"**{user.name}** has been **unbanned**"
                log['user']['name'] = f"{banned_users.user.name}#{banned_users.user.discriminator}"        

        await ctx.respond(embed=embed, ephemeral=True)

        logger.info(log)

def setup(bot):
    bot.add_cog(Unban(bot))