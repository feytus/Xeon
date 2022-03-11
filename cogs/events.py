from discord.ext import commands
from discord import Embed, Member
from discord import Bot

from utils.utils import get_color

from utils.logs import logger

guilds=[809410416685219853, 803981117069852672]


class Events(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, user: Member):
        if user.guild.system_channel is not None:
            embed = Embed(title=f"Welcome {user} !",
                            description=f"{user} joined the server !", color=get_color([0x42c5f5, 0xf54275, 0x70fc6d]))
            embed.set_thumbnail(url=user.avatar)
            embed.timestamp = user.joined_at.timestamp()

        log = {
            "action": "member_join", 
            "user": {"id": user.id, "name": user.display_name+"#"+user.discriminator},
            "guild": user.guild.id
            }

        logger.info(log)

def setup(bot):
    bot.add_cog(Events(bot))