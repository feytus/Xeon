import discord
from discord.ext import commands
from discord.commands import slash_command
from discord import Embed
from discord import ApplicationContext
from discord import Option
from discord import Bot

from twitch_info import get_user_id, get_stream

from os import getenv
from utils.utils import get_color

from utils.logs import logger

guilds=[809410416685219853, 803981117069852672]

headers =  {
        'Accept': 'application/vnd.twitchtv.v5+json',
        'Client-ID': getenv('client_id'),
        'Authorization': 'OAuth ' + getenv('acces_token'),
    }

class Twitch_info(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @slash_command(name="twitch_info", description="Get some informations about a twitch channel", guild_ids=guilds)
    async def twitch_info(self, ctx: ApplicationContext, twitch_channel: Option(str, description="The twitch channel to get informations from")):
        await ctx.defer(ephemeral=True)

        info = get_stream(
            user_id=get_user_id(twitch_channel, getenv('acces_token'), getenv('client_id')),
            headers=headers
        )

        embed = Embed(title="Twitch informations", description=f"**Get some informations about {twitch_channel}**", color=get_color([0x42c5f5, 0xf54275, 0x70fc6d]))
        embed.add_field(name="Display name", value=twitch_channel, inline=True)
        embed.add_field(name="On stream", value=info['on_stream'], inline=True)
        
        if info['on_stream']:
            embed.add_field(name="Game", value=info['game'])
            embed.add_field(name="Viewer count", value=info['viewer_count'])
            embed.set_image(url=info['preview_image'])
            embed.set_thumbnail(url=("https://static-cdn.jtvnw.net/ttv-boxart/" + info['game'].replace(" ", "%20") + ".jpg"))
            embed.set_footer(text=info['date'])


        await ctx.respond(embed=embed, ephemeral=True)

        log = {
            "action": "twitch_info", 
            "author": {"id": ctx.user.id, "name": ctx.user.display_name+"#"+ctx.user.discriminator},
            "twitch_channel": twitch_channel,
            "guild": ctx.guild.id
            }

        logger.info(log)

def setup(bot):
    bot.add_cog(Twitch_info(bot))