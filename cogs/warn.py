import datetime

from discord.ext import commands
from discord.commands import slash_command
from discord import Member, Option, Guild, Embed
from discord import ApplicationContext, Bot
from discord.ext.commands import bot_has_permissions, has_permissions

from utils.utils import get_color
from utils.warning import Warning
from utils.logs import logger

guilds=[809410416685219853, 803981117069852672]


class Warn(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @slash_command(name="warn", description="Warn a member of the discord", guild_ids=guilds)
    @has_permissions(manage_roles=True)
    @bot_has_permissions(send_messages=True, read_messages=True)    
    async def warn(
        self, 
        ctx: ApplicationContext, 
        user: Option(Member, description="The user to warn", required=True),
        reason: Option(str, description="The reason for warning this user", required=True)):
        await ctx.defer(ephemeral=True)

        guild: Guild = ctx.guild

        warning = Warning(self.bot)
        warning.new_member(user=user, guild=guild)
        warning.new_warn(user=user, guild=guild, author=ctx.author, reason=reason)

        embed_user = Embed(description=f"**You received a warning on the server {ctx.guild.name} !**", color=get_color([0xf54531, 0xf57231, 0xf53145]), timestamp = datetime.datetime.utcnow())
        embed_user.add_field(name="Moderator", value=ctx.user.mention, inline=True)
        embed_user.add_field(name="Reason", value=reason, inline=True)
        await user.send(embed=embed_user)

        embed=Embed(
            description=f"**{user}** has been **warned** :white_check_mark:", 
            color=get_color([0x42ff75, 0x42ff75, 0xa9fa52]),
            timestamp = datetime.datetime.utcnow()
            )

        await ctx.respond(embed=embed, ephemeral=True)

        log = {
            "action": "warn", 
            "author": {"id": ctx.user.id, "name": ctx.user.display_name+"#"+ctx.user.discriminator},
            "user": {"id": user.id, "name": user.display_name+"#"+user.discriminator},
            "reason": reason,
            "guild": guild
            }

        logger.info(log)

def setup(bot):
    bot.add_cog(Warn(bot))