import datetime

from discord.ext import commands
from discord.commands import slash_command
from discord import Guild
from discord import Embed
from discord import ApplicationContext, Bot
from discord.ext.commands import bot_has_permissions, has_permissions

from utils.utils import get_color
from utils.logs import logger

guilds=[809410416685219853, 803981117069852672]

class Ban_list(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot  

    @slash_command(name="ban_list", description="Get a list of all banned members", guild_ids=guilds)
    @has_permissions(ban_members=True)
    @bot_has_permissions(send_messages=True, read_messages=True, ban_members=True)
    async def ban_list(self, ctx: ApplicationContext):
        await ctx.defer(ephemeral=True)

        guild: Guild = ctx.guild

        banned_users_list = await guild.bans()

        embed = Embed(
            title="List of banned users", 
            description="Get a list of all banned members", 
            color=get_color([0x42c5f5, 0xf54275, 0x70fc6d]),
            timestamp = datetime.datetime.utcnow())

        for banned_users in banned_users_list:
            embed.add_field(name=f"{banned_users.user.name}#{banned_users.user.discriminator}",
                            value=f"ID : ``{banned_users.user.id}``\nRaison du ban : **{banned_users.reason}**",
                            inline=False)
        
        if len(banned_users_list) == 0:
            embed.description = "There is no **banned user**"

        await ctx.respond(embed=embed, ephemeral=True)

        log = {
            "action": "ban_list", 
            "author": {"id": ctx.user.id, "name": ctx.user.display_name+"#"+ctx.user.discriminator},
            "guild": ctx.guild.id
            }

        logger.info(log)

def setup(bot):
    bot.add_cog(Ban_list(bot))