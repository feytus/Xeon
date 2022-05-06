import datetime

from discord.ext import commands
from discord.ext.commands import bot_has_permissions
from discord.commands import slash_command
from discord import Embed, ApplicationContext, Bot, option

from twitch_info import get_user_id, get_stream, get_access_token

from os import getenv
from utils.color import Color

from utils.logs import logger

guilds=[809410416685219853, 803981117069852672]


class TwitchInfo(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot

    @bot_has_permissions(send_messages=True, read_messages=True)
    @slash_command(name="twitch_info", description="Get some informations about a twitch channel", guild_ids=guilds)
    @option(name="twitch_channel", type=str, description="The twitch channel to get informations from")
    async def twitch_info(self, ctx: ApplicationContext, twitch_channel: str):
        await ctx.defer(ephemeral=True)
        acces_token = get_access_token(client_id=getenv('CLIENT_ID'), client_secret=getenv('CLIENT_SECRET'))

        user_id = get_user_id(
            user_name=twitch_channel,
            client_id=getenv('CLIENT_ID'),
            acces_token=acces_token
            )

        info = get_stream(
            user_id=user_id,
            client_id=getenv('CLIENT_ID'),
            acces_token=acces_token
        )

        embed = Embed(
            title="Twitch informations", 
            description=f"**Get some informations about {twitch_channel}**", 
            color=Color.get_color("lite"),
            timestamp=datetime.datetime.utcnow())

        embed.add_field(name="Display name", value=twitch_channel.capitalize(), inline=True)
        
        if info == "This user is not streaming":
            info = {'type': "Not streaming"}


        if info['type'] == "live":
            embed.description = "**" + info['title'] + "**"
            embed.add_field(name="Statue", value=":red_circle: Streaming", inline=True)
            embed.add_field(name="Game", value=info['game_name'])
            embed.add_field(name="Viewer count", value=info['viewer_count'])
            embed.add_field(name="Language", value="**" + info['language'].upper() + f"** :flag_{info['language']}:")

            thumbail_url = info['thumbnail_url'].replace("{width}", "1080").replace("{height}", "600")
            embed.set_image(url=thumbail_url)
            embed.set_thumbnail(url=("https://static-cdn.jtvnw.net/ttv-boxart/" + info['game_name'].replace(" ", "%20") + ".jpg"))
        else:
             embed.add_field(name="Statue", value="Not streaming", inline=True)

        await ctx.respond(embed=embed, ephemeral=True)

        log = {
            "action": "twitch_info", 
            "author": {"id": ctx.user.id, "name": ctx.user.name+"#"+ctx.user.discriminator},
            "twitch_channel": twitch_channel,
            "guild": {"id": ctx.guild.id, "name": ctx.guild.name}
            }

        logger.info(log)

def setup(bot):
    bot.add_cog(TwitchInfo(bot))