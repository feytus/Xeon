import datetime

from discord.ext import commands
from discord.commands import slash_command
from discord import Option
from discord import ApplicationContext
from discord import Embed
from discord import Member
from discord import Bot
from discord.ext.commands import bot_has_permissions, has_permissions

from utils.embed_logging import EmbedLogging
from utils.config import Config
from utils.logs import logger
from utils.color import Color

guilds=[809410416685219853, 803981117069852672]

class Ban(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.config = Config(bot)
        self.embed_logging = EmbedLogging(bot)

    @slash_command(name="ban", description="Ban a member of the discord", guild_ids=guilds)
    @has_permissions(ban_members=True)
    @bot_has_permissions(send_messages=True, read_messages=True, ban_members=True)
    async def ban(self, ctx: ApplicationContext, user: Option(Member, description="The user to ban"), reason: Option(str, "The reason for banning")):
        await ctx.defer(ephemeral=True)

        embed_user = Embed(description=f"**You have been banned from {ctx.guild.name} !**", color=Color.get_color("sanction"), timestamp=datetime.datetime.utcnow())
        embed_user.add_field(name="Moderator", value=ctx.user.mention, inline=True)
        embed_user.add_field(name="Reason", value=reason, inline=True)
        embed_user.set_thumbnail(url=ctx.guild.icon_url)
        await user.send(embed=embed_user)

        await ctx.guild.ban(user, reason=reason)

        await ctx.respond(
            embed=Embed(
                description=f"**{user.name}** has been **banned** :white_check_mark:", 
                color=0x40e66c,
                timestamp=datetime.datetime.utcnow()), 
            ephemeral=True)

        channel_logging = await self.bot.fetch_channel(
            self.config.get_config(ctx.guild).get("logging_channel")
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
            "id": ctx.user.id, "name": ctx.user.display_name+"#"+ctx.user.discriminator},
            "user": {"id": user.id, "name": user.display_name+"#"+user.discriminator},
            "reason": reason,
            "guild": {"id": ctx.guild.id, "name": ctx.guild.name}}
            
        logger.info(log)

def setup(bot):
    bot.add_cog(Ban(bot))