import datetime

from discord.ext import commands
from discord.commands import slash_command
from discord import ApplicationContext, Embed, Member, Bot, option, default_permissions
from discord.ext.commands import bot_has_permissions, has_permissions

from utils.embed_logging import EmbedLogging
from utils.config import Config
from utils.database import Database
from utils.logs import logger
from utils.color import Color
from utils.utils import guilds_ids

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.embed_logging = EmbedLogging(bot)

    @slash_command(name="ban", description="Ban a member of the discord", guilds_ids=guilds_ids)
    @option(name="user", type=Member, description="The user to ban")
    @option(name="reason", type=str, description="The reason for banning")
    @default_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    @bot_has_permissions(send_messages=True, read_messages=True, ban_members=True)
    async def ban(self, ctx: ApplicationContext, user: Member, reason: str):
        await ctx.defer(ephemeral=True)

        embed_user = Embed(description=f"**You have been banned from {ctx.guild.name} !**", color=Color.get_color("sanction"), timestamp=datetime.datetime.utcnow())
        embed_user.add_field(name="Moderator", value=ctx.user.mention, inline=True)
        embed_user.add_field(name="Reason", value=reason, inline=True)
        embed_user.set_thumbnail(url=ctx.author.display_avatar)
        embed_user.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)
        try:
            await user.send(embed=embed_user)
        except:
            pass

        await ctx.guild.ban(user, reason=reason)

        await ctx.respond(
            embed=Embed(
                description=f"**{user.name}** has been **banned** :white_check_mark:", 
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
                    "action": "ban",
                    "author": ctx.user.id,
                    "user": user.id,
                    "reason": reason
                }
            )
            await channel_logging.send(embed=embed_logging)

        log = {"action": "ban", "author": {
            "id": ctx.user.id, "name": ctx.user.name+"#"+ctx.user.discriminator},
            "user": {"id": user.id, "name": user.name+"#"+user.discriminator},
            "reason": reason,
            "guild": {"id": ctx.guild.id, "name": ctx.guild.name}
            }
            
        logger.info(log)

def setup(bot):
    bot.add_cog(Ban(bot))