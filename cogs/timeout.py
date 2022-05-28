import datetime

from discord.ext import commands
from discord.ext.commands import bot_has_permissions, has_permissions
from discord.commands import slash_command
from discord import Embed, ApplicationContext, Member, Bot, option, default_permissions

from utils.logs import logger
from utils.color import Color
from utils.utils import time_to_second
from utils.config import Config
from utils.database import Database
from utils.embed_logging import EmbedLogging
from utils.utils import guilds_ids


class Timeout(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.embed_logging = EmbedLogging(bot)

    @default_permissions(moderate_members=True)
    @has_permissions(moderate_members=True)
    @bot_has_permissions(send_messages=True, read_messages=True, moderate_members=True)
    @slash_command(name="timeout", description="Timeout a member of the discord")
    @option(name="user", type=Member, description="The user to time out")
    @option(name="duration", type=int)
    @option(name="time", type=str, choices=["second", "minute", "hour", "day", "week", "month"])
    @option(name="reason", type=str, description="The reason for timing him out")
    async def timeout(self, ctx: ApplicationContext, user: Member, duration: int, time: str, reason: str):
        await ctx.defer(ephemeral=True)

        embed_user = Embed(
            description=f"**You have been timed out from {ctx.guild.name} !**", 
            colour=Color.get_color("sanction"), 
            timestamp=datetime.datetime.utcnow())
            
        embed_user.add_field(name="Moderator", value=ctx.user.mention, inline=True)
        embed_user.add_field(name="Reason", value=reason, inline=True)
        embed_user.add_field(name="Duration", value=f"{duration} {time}(s)", inline=True)
        embed_user.set_thumbnail(url=ctx.author.display_avatar)
        embed_user.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)

        time_duration = time_to_second(time, duration)

        await user.timeout_for(time_duration, reason=reason)
        
        try:
            await user.send(embed=embed_user)
        except:
            pass

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
                    "action": "timeout",
                    "author": ctx.user.id,
                    "user": user.id,
                    "duration": duration,
                    "time": time,
                    "reason": reason
                }
            )
            await channel_logging.send(embed=embed_logging)

        await ctx.respond(
            embed=Embed(
                description=f"**{user}** has been **timed out for {duration} {time}** :white_check_mark:",
                color=0x40e66c,
                timestamp=datetime.datetime.utcnow()),
            ephemeral=True)

        log = {
            "action": "timeout", 
            "author": {"id": ctx.user.id, "name": ctx.user.name+"#"+ctx.user.discriminator},
            "user": {"id": user.id, "name": user.name+"#"+ctx.user.discriminator}, 
            "duration": duration, 
            "time": time, 
            "reason": reason,
            "guild": {"id": ctx.guild.id, "name": ctx.guild.name}
            }

        logger.info(log)


def setup(bot):
    bot.add_cog(Timeout(bot))
