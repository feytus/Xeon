import datetime

from discord.ext import commands
from discord.commands import slash_command
from discord import Bot, Embed, ApplicationContext, Member, option
from discord.ext.commands import bot_has_permissions, has_permissions

from utils.color import Color
from utils.logs import logger

guilds=[809410416685219853, 803981117069852672]

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @has_permissions(manage_roles=True)
    @bot_has_permissions(send_messages=True, read_messages=True)
    @slash_command(name="user_info", description="Get some informations about a member of the discord", guild_ids=guilds)
    @option(name="user", type=Member, description="The user to get informations from", required=False)
    async def user_info(self, ctx: ApplicationContext, user: Member):
        await ctx.defer(ephemeral=True)

        if user is None:
            user = ctx.author

        embed = Embed(
            title="User informations",
            description=f"**Get some informations** about {user.mention}", 
            color=Color.get_color("lite"),
            timestamp=datetime.datetime.utcnow())
            
        embed.add_field(name="Full nickname", value=user, inline=True)
        embed.add_field(name="ID", value=user.id, inline=True)
        embed.add_field(name="Roles in the server",
                        value=len(user.roles) - 1, inline=False)
        embed.add_field(name="Highest role",
                        value=user.top_role, inline=False)
        embed.add_field(name="Join the server", value=user.joined_at.strftime('%Y-%m-%d-%H'))
        embed.set_thumbnail(url=user.display_avatar)

        await ctx.respond(embed=embed, ephemeral=True)
        
        log = {
            "action": "user_info", 
            "author": {"id": ctx.user.id, "name": ctx.user.name+"#"+ctx.user.discriminator},
            "user": {"id": user.id, "name": user.name+"#"+user.discriminator},
            "guild": {"id": ctx.guild.id, "name": ctx.guild.name}
            }

        logger.info(log)

def setup(bot):
    bot.add_cog(UserInfo(bot))