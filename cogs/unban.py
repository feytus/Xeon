import datetime

from discord.ext import commands
from discord.commands import slash_command
from discord import User, Guild, Embed, ApplicationContext, Bot, option, default_permissions
from discord.ext.commands import bot_has_permissions, has_permissions

from utils.config import Config
from utils.database import Database
from utils.embed_logging import EmbedLogging
from utils.color import Color
from utils.logs import logger
from utils.utils import guilds_ids

class Unban(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.embed_logging = EmbedLogging(bot)

    @default_permissions(ban_members=True)
    @has_permissions(ban_members=True)
    @bot_has_permissions(send_messages=True, read_messages=True, ban_members=True)
    @slash_command(name="unban", description="Unban a banned member")
    @option(name="user", type=str, description="The user to unban : exemple#1234 or the user ID")
    @option(name="reason", type=str, description="The reason for unbanning")
    async def unban(self, ctx: ApplicationContext, user: str, reason: str="No reason given"):
        await ctx.defer(ephemeral=True)

        guild: Guild = ctx.guild

        banned_users_list = await guild.bans().flatten()

        embed = Embed(title="Error", description="**This user is not banned** :white_check_mark:", colour=Color.get_color("sanction"), timestamp=datetime.datetime.utcnow())

        log = {
            "action": "unban", 
            "author": {"id": ctx.user.id, "name": ctx.user.name+"#"+ctx.user.discriminator},
            "user": {},
            "reason": reason,
            "guild": {"id": ctx.guild.id, "name": ctx.guild.name}
            }

        for banned_users in banned_users_list:
            user: User = await self.bot.fetch_user(banned_users.user.id)
            if user == str(banned_users.user.id):
                await guild.unban(user, reason)

                embed.title = "Unban"
                embed.description = f"**{user.name}** has been **unbanned**"

                log['user']['id'] = user.id

            elif str(user) == f"{banned_users.user.name}#{banned_users.user.discriminator}":
                await guild.unban(user=user, reason=reason)

                embed.title = "Unban"
                embed.description = f"**{user.name}** has been **unbanned**"

                log['user']['name'] = f"{banned_users.user.name}#{banned_users.user.discriminator}"        

        await ctx.respond(embed=embed, ephemeral=True)

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
                    "action": "unban",
                    "author": ctx.user.id,
                    "user": user.id,
                    "reason": reason
                }
            )
            await channel_logging.send(embed=embed_logging)

        logger.info(log)

def setup(bot):
    bot.add_cog(Unban(bot))