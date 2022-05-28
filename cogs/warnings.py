import datetime

from discord.ext import commands
from discord.commands import slash_command
from discord import Member, Guild, Embed, ApplicationContext, Bot, default_permissions, option
from discord.ext.commands import bot_has_permissions, has_permissions

from utils.config import Config
from utils.database import Database
from utils.embed_logging import EmbedLogging
from utils.color import Color
from utils.warning import Warning
from utils.logs import logger
from utils.utils import guilds_ids


class Warn(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.embed_logging = EmbedLogging(bot)
        self.warning = Warning()

    @default_permissions(manage_roles=True)
    @has_permissions(manage_roles=True)
    @bot_has_permissions(send_messages=True, read_messages=True)  
    @slash_command(name="warn", description="Warn a member of the discord", guilds_ids=guilds_ids)  
    @option(name="user", type=Member, description="The user to warn")
    @option(name="reason", type=str, description="The reason for warning")
    async def warn(self, ctx: ApplicationContext, user: Member, reason: str):
        await ctx.defer(ephemeral=True)

        guild: Guild = ctx.guild

        if not Database.check_config(guild.id):
            warning = Warning(self.bot)
            warning.new_member(user=user, guild=guild)
            warning.new_warn(user=user, guild=guild, author=ctx.author, reason=reason)
        else:
            Database.add_warnings(user_id=user.id, guild_id=guild.id, author_id=ctx.author.id, reason=reason)

        embed_user = Embed(description=f"**You received a warning on the server {ctx.guild.name} !**", color=Color.get_color("sanction"), timestamp=datetime.datetime.utcnow())
        embed_user.add_field(name="Moderator", value=ctx.user.mention, inline=True)
        embed_user.add_field(name="Reason", value=reason, inline=True)
        embed_user.set_thumbnail(url=ctx.author.display_avatar)
        embed_user.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon)
        try:
            await user.send(embed=embed_user)
        except:
            pass

        embed=Embed(
            description=f"**{user}** has been **warned** :white_check_mark:", 
            color=0x40e66c,
            timestamp=datetime.datetime.utcnow()
            )

        await ctx.respond(embed=embed, ephemeral=True)

        channel_logging = self.bot.get_channel(Config.get_config(ctx.guild).get("logging_channel"))

        if channel_logging is not None:
            embed_logging = self.embed_logging.get_embed(
                data={
                    "action": "warn",
                    "author": ctx.user.id,
                    "user": user.id,
                    "reason": reason
                }
            )
            await channel_logging.send(embed=embed_logging)

        log = {
            "action": "warn", 
            "author": {"id": ctx.user.id, "name": ctx.user.name+"#"+ctx.user.discriminator},
            "user": {"id": user.id, "name": user.name+"#"+user.discriminator},
            "reason": reason,
            "guild": {"id": guild.id, "name": guild.name}
            }

        logger.info(log)

    @has_permissions(manage_roles=True)
    @bot_has_permissions(send_messages=True, read_messages=True)
    @slash_command(name="warnings", description="Get a list of warnings from a member of the discord", guilds_ids=guilds_ids)
    @option(name="user", type=Member, description="The user to get the warnings")
    async def warnings(self, ctx: ApplicationContext, user: Member):
        await ctx.defer(ephemeral=True)

        guild: Guild = ctx.guild
        
        if not Database.check_config(guild.id):
            self.warning.new_member(user=user, guild=guild)
            warnings = self.warning.get_warnings(user=user, guild=guild)
        else:
            warnings = Database.get_warnings(user_id=user.id, guild_id=guild.id)

        embed=Embed(
            title="Warnings",
            description=f"{user} has no warnings",
            color=Color.get_color("lite"),
            timestamp=datetime.datetime.utcnow())

        if warnings != []:
            embed.description=f"**List of all the warnings from {user.mention}** :\n\n"

        for warn in warnings:
            author = await self.bot.fetch_user(warn.get("author_id"))
            date = datetime.datetime.fromtimestamp(warn.get("date"))
            
            embed.description += f":calendar: **{date.strftime('%d/%m/%Y à %H:%M')}**\n:crossed_swords: **Moderator** : {author.mention}```{warn['reason']}``` :id: : ``{warn['id']}``\n\n"
        await ctx.respond(embed=embed, ephemeral=True)

        log = {
            "action": "warnings", 
            "author": {"id": ctx.user.id, "name": ctx.user.name+"#"+ctx.user.discriminator},
            "user": {"id": user.id, "name": user.name+"#"+user.discriminator},
            "guild": {"id": guild.id, "name": guild.name}
            }

        logger.info(log)

    @has_permissions(manage_roles=True)
    @bot_has_permissions(send_messages=True, read_messages=True)  
    @slash_command(name="remove_warning", description="Remove a warning from a member of the discord", guilds_ids=guilds_ids)
    @option(name="user", type=Member, description="The user to remove the warning")
    @option(name="warning_id", type=int, description="The id of the warning to remove", required=False)
    async def remove_warning(self, ctx: ApplicationContext, user: Member, warning_id: int):
        await ctx.defer(ephemeral=True)

        guild: Guild = ctx.guild

        if not Database.check_config(guild.id):
            self.warning.new_member(user=user, guild=guild)
            self.warning.remove_warning(guild=guild, user=user, warning_index=warning_id)
        else:
            Database.remove_warning(user_id=user.id, guild_id=guild.id, warning_id=warning_id)

        if warning_id is not None:
            embed=Embed(
                description=f"You have **removed a warn from {user}** :white_check_mark:", 
                color=0x40e66c,
                timestamp=datetime.datetime.utcnow())
        else:
            embed=Embed(
                description=f"You have **removed all the warnings from {user}** :white_check_mark:", 
                color=0x40e66c,
                timestamp=datetime.datetime.utcnow())

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
                    "action": "remove_warning",
                    "author": ctx.user.id,
                    "user": user.id,
                }
            )
            await channel_logging.send(embed=embed_logging)

        log = {
            "action": "remove_warning", 
            "author": {"id": ctx.user.id, "name": ctx.user.name+"#"+ctx.user.discriminator},
            "user": {"id": user.id, "name": user.name+"#"+user.discriminator},
            "warning_id": warning_id,
            "guild": {"id": guild.id, "name": guild.name}
            }

        logger.info(log)
        
def setup(bot):
    bot.add_cog(Warn(bot))
