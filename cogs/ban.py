import datetime

from discord.ext import commands
from discord.commands import slash_command
from discord import Option
from discord import ApplicationContext
from discord import Embed
from discord import Member
from discord import Bot
from discord.ext.commands import bot_has_permissions, has_permissions

from utils.logs import logger
from utils.utils import get_color

guilds=[809410416685219853, 803981117069852672]

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @slash_command(name="ban", description="Ban a member of the discord", guild_ids=guilds)
    @has_permissions(ban_members=True)
    @bot_has_permissions(send_messages=True, read_messages=True, ban_members=True)
    async def ban(self, ctx: ApplicationContext, user: Option(Member, description="The user to ban"), reason: Option(str, "The reason for banning")):
        await ctx.defer(ephemeral=True)

        embed_user = Embed(description=f"**You have been banned from {ctx.guild.name} !**", color=get_color([0xf54531, 0xf57231, 0xf53145]), timestamp = datetime.datetime.utcnow())
        embed_user.add_field(name="Moderator", value=ctx.user.mention, inline=True)
        embed_user.add_field(name="Reason", value=reason, inline=True)
        await user.send(embed=embed_user)

        await ctx.guild.ban(user, reason=reason)

        await ctx.respond(
            embed=Embed(
                description=f"**{user.name}** has been **banned** :white_check_mark:", 
                color=get_color([0x42ff75, 0x42ff75, 0xa9fa52]),
                timestamp = datetime.datetime.utcnow()), 
            ephemeral=True)

        log = {"action": "ban", "author": {
            "id": ctx.user.id, "name": ctx.user.display_name+"#"+ctx.user.discriminator},
            "user": {"id": user.id, "name": user.display_name+"#"+user.discriminator},
            "reason": reason,
            "guild": ctx.guild.id}
            
        logger.info(log)

def setup(bot):
    bot.add_cog(Ban(bot))