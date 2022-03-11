import datetime

from discord.ext import commands
from discord.commands import slash_command
from discord import Embed
from discord import ApplicationContext
from discord import Option
from discord import Bot

from twitch_info import get_user_id, get_stream, get_access_token

from os import getenv
from utils.utils import get_color

from utils.logs import logger

guilds=[809410416685219853, 803981117069852672]


class Twitch_info(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @slash_command(name="twitch_info", description="Get some informations about a twitch channel", guild_ids=guilds)
    async def twitch_info(self, ctx: ApplicationContext, twitch_channel: Option(str, description="The twitch channel to get informations from")):
        await ctx.defer(ephemeral=True)
        acces_token = get_access_token(client_id=getenv('client_id'), client_secret=getenv('client_secret'))

        user_id = get_user_id(
            user_name=twitch_channel,
            client_id=getenv('client_id'),
            acces_token=acces_token
            )

        info = get_stream(
            user_id=user_id,
            client_id=getenv('client_id'),
            acces_token=acces_token
        )

        embed = Embed(
            title="Twitch informations", 
            description=f"**Get some informations about {twitch_channel}**", 
            color=get_color([0x42c5f5, 0xf54275, 0x70fc6d]),
            timestamp = datetime.datetime.utcnow())
        embed.add_field(name="Display name", value=twitch_channel, inline=True)
        
        if info == "This user is not streaming":
            info = {'type': "Not streaming"}

        if info['type'] == "live":
            embed.description = "**" + info['title'] + "**"
            embed.add_field(name="Statue", value="Streaming", inline=True)
            embed.add_field(name="Game", value=info['game_name'])
            embed.add_field(name="Viewer count", value=info['viewer_count'])
            embed.add_field(name="language", value=info['language'] + f" :flag_{info['language']}:")

            thumbail_url = info['thumbnail_url'].replace("{width}", "1080").replace("{height}", "600")
            embed.set_image(url=thumbail_url)
            embed.set_thumbnail(url=("https://static-cdn.jtvnw.net/ttv-boxart/" + info['game_name'].replace(" ", "%20") + ".jpg"))
            embed.set_footer(text=info['started_at'])
        else:
             embed.add_field(name="Statue", value="Not streaming", inline=True)

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