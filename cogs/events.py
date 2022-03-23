import datetime

from discord.ext import commands
from discord import Embed, Member, Game, Status
from discord import Bot, ApplicationContext

from utils.utils import colors

from utils.logs import logger

guilds=[809410416685219853, 803981117069852672]


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

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

        activity = Game(name="https://github.com/feytus/Xeon", type=3)
        await self.bot.change_presence(status=Status.online, activity=activity)
        
        log = {"on_ready": "bot is ready"}
        logger.info(log)

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: ApplicationContext,  error):
        await ctx.respond(
            embed=Embed(
                title="Error",
                description=f"**{error}**", color=colors["sanction"],
                timestamp=datetime.datetime.utcnow(),
                color = colors['lite']
                ),
                ephemeral=True
            )

        log = {"command": ctx.command, "author": ctx.author.id, "error": error}
        logger.warning(log)

    @commands.Cog.listener()
    async def on_member_join(self, user: Member):
        user = user.guild.get_member(user.id)

        if user.guild.system_channel is not None:
            embed = Embed(title=f"Welcome {user} !",
                            description=f"**{user.mention} joined the server !**", color=colors['lite'])
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

def setup(bot):
    bot.add_cog(Events(bot))