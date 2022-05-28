import datetime

from discord.ext import commands
from discord.commands import slash_command
from discord import Attachment, Member, Option, Embed, ApplicationContext, Bot, option
from discord.ext.commands import bot_has_permissions, has_permissions

from utils.embed_logging import EmbedLogging
from utils.logs import logger
from utils.config import Config
from utils.utils import guilds_ids

class Report(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.embed_logging = EmbedLogging(bot)

    @slash_command(name="report", description="Report a member of the discord", guilds_ids=guilds_ids)
    @option(name="user", type=Member, description="The user to report")
    @option(name="reason", type=str, description="The reason for reporting")
    @option(name="proof", type=Attachment, description="The proof of the report", required=False)
    @bot_has_permissions(send_messages=True, read_messages=True, manage_messages=True)
    async def report(self, ctx: ApplicationContext, user: Member, reason: str, proof: Attachment):
        await ctx.defer(ephemeral=True)

        await ctx.respond(
            embed=Embed(
                description=f"**{user}** has been **reported** :white_check_mark:", 
                color=0x40e66c,
                timestamp=datetime.datetime.utcnow()),
            ephemeral=True)
        
        Config.config_element(ctx.guild, "channel_report", value=ctx.channel.id)

        channel_report = self.bot.get_channel(
            Config.get_config(ctx.guild).get("channel_report")
            )

        if channel_report is Attachment:
            embed_logging = self.embed_logging.get_embed(
                data={
                    "action": "report",
                    "author": ctx.user.id,
                    "user": user.id,
                    "reason": reason,
                }
            )
            if proof is not None:
                proof = await proof.to_file()
                await channel_report.send(embed=embed_logging, file=proof)
            else:
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