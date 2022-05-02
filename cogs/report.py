import datetime

from discord.ext import commands
from discord.commands import slash_command
from discord import Member, Option, Embed, ApplicationContext, Bot
from discord.ext.commands import bot_has_permissions, has_permissions

from utils.embed_logging import EmbedLogging
from utils.logs import logger
from utils.config import Config

guilds=[809410416685219853, 803981117069852672]

class Report(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.config = Config()
        self.embed_logging = EmbedLogging(bot)

    @slash_command(name="report", description="Report a member of the discord", guild_ids=guilds)
    @has_permissions(manage_messages=True)
    @bot_has_permissions(send_messages=True, read_messages=True, manage_messages=True)
    async def report(
        self, 
        ctx: ApplicationContext, 
        user: Option(Member, description="The user to report"), 
        reason: Option(str, description="The reason for reporting"), 
        proof: Option(str, description="The proof of the report (must be an url)", required=False)):
        await ctx.defer(ephemeral=True)

        await ctx.respond(
            embed=Embed(
                description=f"**{user}** has been **reported** :white_check_mark:", 
                color=0x40e66c,
                timestamp=datetime.datetime.utcnow()),
            ephemeral=True)
        
        self.config.config_element(ctx.guild, "channel_report", value=ctx.channel.id)

        channel_report = self.bot.get_channel(
            self.config.get_config(ctx.guild).get("channel_report")
            )

        if channel_report is not None:
            embed_logging = self.embed_logging.get_embed(
                data={
                    "action": "report",
                    "author": ctx.user.id,
                    "user": user.id,
                    "reason": reason,
                    "proof": proof
                }
            )
            await channel_report.send(embed=embed_logging)

        log = {
            "action": "report",
            "author": {"id": ctx.user.id, "name": ctx.user.name+"#"+ctx.user.discriminator},
            "user": {"id": user.id, "name": user.name+"#"+ctx.user.discriminator}, 
            "reason": reason,
            "guild": {"id": ctx.guild.id, "name": ctx.guild.name}
            }

        logger.info(log)

def setup(bot):
    bot.add_cog(Report(bot))