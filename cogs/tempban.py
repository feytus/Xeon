import datetime

from datetime import timedelta

from discord.ext import commands
from discord.commands import slash_command
from discord import Bot, Embed
from discord import ApplicationContext
from discord import Option
from discord import Member
from discord.ext.commands import bot_has_permissions, has_permissions

from asyncio import sleep

from utils.color import Color
from utils.utils import time_to_second
from utils.logs import logger
from utils.embed_logging import EmbedLogging
from utils.config import Config

guilds=[809410416685219853, 803981117069852672]

class Tempban(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.config = Config(bot)
        self.embed_logging = EmbedLogging(bot)

    @slash_command(name="tempban", description="Temporarily ban member of the discord", guild_ids=guilds)
    @has_permissions(moderate_members=True)
    @bot_has_permissions(send_messages=True, read_messages=True, moderate_members=True)
    async def tempban(
        self, ctx: ApplicationContext, user: Option(Member, description="The user to temporarily ban"), duration: int, time: Option(str,
            choices=["second", "minute", "hour", "day", "week", "month"]),
            reason: Option(str, description="The reason for banning temporarily")):
        await ctx.defer(ephemeral=True)

        embed_user = Embed(description=f"**You have been temporarily banned from {ctx.guild.name} !**", color=Color.get_color("sanction"), timestamp=datetime.datetime.utcnow())
        
        embed_user.add_field(name="Moderator", value=ctx.user.mention, inline=True)
        embed_user.add_field(name="Reason", value=reason, inline=True)
        embed_user.add_field(name="Duration", value=f"{duration} {time}(s)", inline=True)
        embed_user.set_thumbnail(url=ctx.author.display_avatar)
        embed_user.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)
        await user.send(embed=embed_user)

        time_duration: timedelta = time_to_second(time, duration)
        await ctx.guild.ban(user, reason=reason)

        channel_logging = await self.bot.fetch_channel(
            self.config.get_config(ctx.guild).get("logging_channel")
        )

        if channel_logging is not None:
            embed_logging = self.embed_logging.get_embed(
                data={
                    "action": "tempban",
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
                description=f"**{user}** has been **banned for {duration} {time}** :white_check_mark:", 
                color=0x40e66c,
                timestamp=datetime.datetime.utcnow()), 
            ephemeral=True)

        await sleep(time_duration.total_seconds())
        await ctx.guild.unban(user, reason="End of the ban")

        log = {
            "action": "tempban", 
            "author": {"id": ctx.user.id, "name": ctx.user.display_name+"#"+ctx.user.discriminator}, 
            "user": {"id": user.id, "name": user.display_name+"#"+ctx.user.discriminator}, 
            "duration": duration, 
            "time": time, 
            "reason": reason,
            "guild": {"id": ctx.guild.id, "name": ctx.guild.name}
            }

        logger.info(log)
        
def setup(bot):
    bot.add_cog(Tempban(bot))