import discord
from discord.ext import commands
from discord.commands import slash_command
from discord import Bot, Embed
from discord import ApplicationContext
from discord import Option
from discord import Member
from discord.ext.commands import bot_has_permissions, has_permissions

from utils.utils import get_color
from utils.logs import logger

guilds=[809410416685219853, 803981117069852672]

class User_info(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @slash_command(name="user_info", description="Get some informations about a member of the discord", guild_ids=guilds)
    @has_permissions(manage_roles=True)
    @bot_has_permissions(send_messages=True, read_messages=True)
    async def user_info(self, ctx: ApplicationContext, user: Option(Member, description="The user to get informations from", required=False)):
        await ctx.defer(ephemeral=True)

        if user is None:
            user: Member = ctx.user

        embed = Embed(title="User informations",
                            description=f"**Get some informations** about {user.mention}", color=get_color([0x42c5f5, 0xf54275, 0x70fc6d]))
        embed.add_field(name="Full nickname", value=user, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Roles in the server",
                        value=len(user.roles) - 1, inline=False)
        embed.add_field(name="Highest role",
                        value=user.top_role, inline=False)
        embed.add_field(name="Join the server", value=user.joined_at.strftime('%Y-%m-%d-%H'))
        embed.set_thumbnail(url=user.avatar)

        await ctx.respond(embed=embed, ephemeral=True)

        log = {
            "action": "user_info", 
            "author": {"id": user.id, "name": user.display_name+"#"+user.discriminator},
            "guild": ctx.guild.id
            }

        logger.info(log)

def setup(bot):
    bot.add_cog(User_info(bot))