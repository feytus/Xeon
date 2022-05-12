import datetime

from discord.ext import commands
from discord.commands import slash_command
from discord.ext.commands import bot_has_permissions, has_permissions
from discord import Member, Bot, Embed, ApplicationContext, option, default_permissions

from utils.embed_logging import EmbedLogging
from utils.config import Config
from utils.color import Color
from utils.logs import logger

guilds=[809410416685219853, 803981117069852672]

class Kick(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.config = Config()
        self.embed_logging = EmbedLogging(bot)

    @slash_command(name="kick", description="Kick a member of the discord", guild_ids=guilds)
    @option(name="user", type=Member, description="The user to kick")
    @option(name="reason", type=str, description="The reason for kicking")
    @default_permissions(kick_members=True)
    @has_permissions(kick_members=True)
    @bot_has_permissions(send_messages=True, read_messages=True, kick_members=True)
    async def kick(self, ctx: ApplicationContext, user: Member, reason: str):
        await ctx.defer(ephemeral=True)

        embed_user = Embed(description=f"**You have been kicked from {ctx.guild.name} !**", color=Color.get_color("sanction"), timestamp=datetime.datetime.utcnow())
        embed_user.add_field(name="Moderator", value=ctx.user.mention, inline=True)
        embed_user.add_field(name="Reason", value=reason, inline=True)
        embed_user.set_thumbnail(url=ctx.author.display_avatar)
        embed_user.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)
        await user.send(embed=embed_user)

        await ctx.guild.kick(user=user, reason=reason)

        await ctx.respond(
            embed=Embed(
                description=f"**{user}** has been **kicked** :white_check_mark:", 
                color=0x40e66c,
                timestamp=datetime.datetime.utcnow()), 
            ephemeral=True)

        channel_logging = self.bot.get_channel(
            self.config.get_config(ctx.guild).get("logging_channel")
        )

        if channel_logging is not None:
            embed_logging = self.embed_logging.get_embed(
                data={
                    "action": "kick",
                    "author": ctx.user.id,
                    "user": user.id,
                    "reason": reason
                }
            )
            await channel_logging.send(embed=embed_logging)

        log = {"action": "kick", "author": {
            "id": ctx.user.id, "name": ctx.user.name+"#"+ctx.user.discriminator},
            "user": {"id": user.id, "name": user.name+"#"+user.discriminator},
            "reason": reason,
            "guild": {"id": ctx.guild.id, "name": ctx.guild.name}
            }

        logger.info(log)

def setup(bot):
    bot.add_cog(Kick(bot))