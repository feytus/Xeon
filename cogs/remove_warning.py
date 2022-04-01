import datetime

from discord.ext import commands
from discord.commands import slash_command
from discord import Member, Option, Guild
from discord import Embed
from discord import ApplicationContext, Bot
from discord.ext.commands import bot_has_permissions, has_permissions

from utils.warning import Warning
from utils.embed_logging import EmbedLogging
from utils.config import Config
from utils.logs import logger

guilds=[809410416685219853, 803981117069852672]


class Remove_warning(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.config = Config(bot)
        self.warning = Warning(bot)
        self.embed_logging = EmbedLogging(bot)

    @slash_command(name="remove_warning", description="Remove a warning from a member of the discord", guild_ids=guilds)
    @has_permissions(manage_roles=True)
    @bot_has_permissions(send_messages=True, read_messages=True)    
    async def remove_warning(
        self, 
        ctx: ApplicationContext, 
        user: Option(Member, description="The user to warn", required=True),
        warning_number: Option(int, description="The number of the warning", required=False)):
        await ctx.defer(ephemeral=True)

        guild: Guild = ctx.guild

        self.warning.new_member(user=user, guild=guild)
        self.warning.remove_warning(guild=guild, user=user, warning_index=warning_number)

        if warning_number is not None:
            embed=Embed(
                description=f"You have **removed a warn from {user}** :white_check_mark:", 
                color=0x40e66c,
                timestamp=datetime.datetime.utcnow())
        else:
            embed=Embed(
                description=f"You have **removed all warnings from {user}** :white_check_mark:", 
                color=0x40e66c,
                timestamp=datetime.datetime.utcnow())

        await ctx.respond(embed=embed, ephemeral=True)

        channel_logging = self.bot.get_channel(
            self.config.get_config(ctx.guild).get("channel_logging")
            )

        if channel_logging is not None:
            embed_logging = self.embed_logging.get_embed(
                data={
                    "action": "remove_warning",
                    "author": ctx.user.id,
                    "user": user.id,
                }
            )
            await channel_logging.send(embed=embed_logging)

        log = {
            "action": "remove_warning", 
            "author": {"id": ctx.user.id, "name": ctx.user.display_name+"#"+ctx.user.discriminator},
            "user": {"id": user.id, "name": user.display_name+"#"+user.discriminator},
            "warning_number": warning_number,
            "guild": {"id": guild.id, "name": guild.name}
            }

        logger.info(log)

def setup(bot):
    bot.add_cog(Remove_warning(bot))