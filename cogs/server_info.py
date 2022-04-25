import datetime

from discord.ext import commands
from discord.commands import slash_command
from discord import Bot, Embed, ApplicationContext
from discord.ext.commands import bot_has_permissions, has_permissions

from utils.color import Color
from utils.logs import logger

guilds=[809410416685219853, 803981117069852672]

class Server_Info(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @slash_command(name="server_info", description="Get some informations about the discord", guild_ids=guilds)
    @has_permissions(manage_roles=True)
    @bot_has_permissions(send_messages=True, read_messages=True)
    async def server_info(self, ctx: ApplicationContext):
        await ctx.defer(ephemeral=True)

        embed = Embed(
            title=ctx.guild.name,
            description=f"**Get some informations** about the discord", 
            color=Color.get_color("lite"),
            timestamp=datetime.datetime.utcnow())
            
        embed.add_field(name="Owner", value=ctx.guild.owner, inline=True)
        embed.add_field(name="ID", value=ctx.guild.id, inline=True)
        embed.add_field(name="Members", value=len(ctx.guild.members), inline=True)
        embed.add_field(name="Category", value=len(ctx.guild.categories), inline=True)
        embed.add_field(name="Channels", value=len(ctx.guild.channels), inline=True)
        embed.add_field(name="Roles", value=len(ctx.guild.roles), inline=True)
        embed.add_field(name="Region", value=ctx.guild.region, inline=True)
        embed.add_field(name="Created at", value=ctx.guild.created_at.strftime('%Y-%m-%d'))
        embed.set_thumbnail(url=ctx.guild.icon)

        await ctx.respond(embed=embed, ephemeral=True)
        
        log = {
            "action": "server_info", 
            "author": {"id": ctx.user.id, "name": ctx.user.name+"#"+ctx.user.discriminator},
            "guild": {"id": ctx.guild.id, "name": ctx.guild.name}
            }

        logger.info(log)

def setup(bot):
    bot.add_cog(Server_Info(bot))