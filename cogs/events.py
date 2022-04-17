import datetime
import discord

from discord.ext import commands
from discord import Embed, Member, Guild
from discord import Bot, ApplicationContext

from utils.warning import Warning
from utils.color import Color
from utils.config import Config
from utils.logs import logger

guilds=[809410416685219853, 803981117069852672]


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.config = Config(bot)
        self.warning = Warning(bot)

        self.xeon = """
    ██╗  ██╗███████╗ █████╗ ███╗  ██╗
    ╚██╗██╔╝██╔════╝██╔══██╗████╗ ██║
     ╚███╔╝ █████╗  ██║  ██║██╔██╗██║
     ██╔██╗ ██╔══╝  ██║  ██║██║╚████║
    ██╔╝╚██╗███████╗╚█████╔╝██║ ╚███║
    ╚═╝  ╚═╝╚══════╝ ╚════╝ ╚═╝  ╚══╝
    """
    @commands.Cog.listener()
    async def on_ready(self):
        print(self.xeon)
        logger.info(msg="latency : " + str(round(self.bot.latency * 1000)) + " ms")

        for guild in self.bot.guilds:
            if not self.config.is_config(guild):
                self.config.config_server(guild)
                logger.info({"action": "configuration", "guild": {"id": guild.id, "name": guild.name}})

        log = {"action": "on_ready"}

        logger.info(log)

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: ApplicationContext, error):
        await ctx.respond(
            embed=Embed(
                title="Error",
                description=f"**{error}**", 
                color=Color.get_color("sanction"),
                timestamp=datetime.datetime.utcnow(),
                ),
                ephemeral=True
            )

        log = {"command": ctx.command, "author": ctx.author.id, "error": error}
        logger.warning(log)

    @commands.Cog.listener()
    async def on_error(self, ctx: ApplicationContext, error):
        if error is discord.errors.HTTPException:
            ctx.respond(embed=Embed(
                title="Error",
                description=f"**Whoops ! try again later**", 
                color=Color.get_color("sanction"),
                timestamp=datetime.datetime.utcnow(),
                ),
                ephemeral=True
            )

    @commands.Cog.listener()
    async def on_member_join(self, user: Member):
        user = user.guild.get_member(user.id)

        self.warning.new_member(user, user.guild)

        if user.guild.system_channel is not None:
            embed = Embed(title=f"Welcome {user} !",
                            description=f"**{user.mention} joined the server !**", color=Color.get_color("lite"))
            embed.set_author(name=user.guild.name, icon_url=user.guild.icon)
            embed.set_thumbnail(url=user.display_avatar)
            embed.timestamp = user.joined_at

            await user.guild.system_channel.send(embed=embed)

        log = {
            "action": "on_member_join", 
            "user": {"id": user.id, "name": user.display_name+"#"+user.discriminator},
            "guild": user.guild.id
            }

        logger.info(log)
    
    @commands.Cog.listener()
    async def on_member_update(self, before: Member, after: Member):
        info_before = {
            "nickname": before,
            "roles": before.roles,
            "pending": before.pending,
            "communication_disabled_until": before.communication_disabled_until,
            "timed_out": before.timed_out
        }

        info_after = {
            "nickname": after,
            "roles": after.roles,
            "pending": after.pending,
            "communication_disabled_until": after.communication_disabled_until,
            "timed_out": after.timed_out
        }

        for key in info_after.keys():
            if info_after[key] != info_before[key]:
                print(key, info_before[key], "-", info_after[key])

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild):
        if not self.config.is_config(guild):
            self.config.config_server(guild)
            logger.info({"action": "configuration", "guild": {"id": guild.id, "name": guild.name}})
            
        log = {
            "action": "on_guild_join",
            "guild": {"id": guild.id, "name": guild.name},
            "is configured": self.config.is_config(guild)
        }

        logger.info(log)   

def setup(bot):
    bot.add_cog(Events(bot))