import datetime
import discord
import random
import string
import asyncio
import pyimgur
import os

from captcha.image import ImageCaptcha

from discord.ext import commands
from discord import Bot, ApplicationContext, Embed, Member, Guild, PermissionOverwrite, Message

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
        self.imgur = pyimgur.Imgur(os.getenv("IMGUR_CLIENT_ID"))

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
            print(guild, self.config.is_config(guild))
            if not self.config.is_config(guild):
                self.config.config_server(guild)
                logger.info({"action": "configuration", "guild": {"id": guild.id, "name": guild.name}})

        log = {"action": "on_ready"}

        logger.info(log)

    #@commands.Cog.listener()
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

    #@commands.Cog.listener()
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

        log = {"command": ctx.command, "author": ctx.author.id, "error": error}
        logger.warning(log)

    async def captcha_check(self, user: Member):
        if len(os.listdir(f"data/{guild.id}/captcha/")) >= 10:
            for file in os.listdir(f"data/{guild.id}/captcha/"):
                os.remove(f"data/{guild.id}/captcha/{file}")

        guild = user.guild

        overwrites = {
            guild.default_role: PermissionOverwrite(read_messages=False),
            guild.me: PermissionOverwrite(read_messages=True),
            guild.get_member(user.id): PermissionOverwrite(read_messages=True),
        }
        channel = await guild.create_text_channel(name=user.name+"#"+user.discriminator, overwrites=overwrites)
        
        file_name = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S") + ".png"

        letters = string.ascii_uppercase
        result_str = ''.join(random.choice(letters) for i in range(5))

        image = ImageCaptcha()

        image.write(result_str, f"data/{guild.id}/captcha/{file_name}")

        uploaded_image = self.imgur.upload_image(path=f"data/{guild.id}/captcha/{file_name}", title=file_name)
        

        embed = Embed(title="Captcha", description=f"{user.mention} Please send **{result_str}**", color=discord.Color.random())
        embed.set_image(url=uploaded_image.link)
        message_captcha = await channel.send(embed=embed)

        try:
            response: Message = await self.bot.wait_for("message", check=lambda response: response.author == user, timeout=30)
        except asyncio.TimeoutError:
            await user.kick()
        
        if response.content == result_str:
            await user.add_roles(user.guild.get_role(871205238546255922))
            await message_captcha.delete()
            await response.delete()
        else:
            await user.kick()
            await message_captcha.delete()
            await response.delete()

        await channel.delete()

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

        await self.captcha_check(user)
        log = {
            "action": "on_member_join", 
            "user": {"id": user.id, "name": user.name+"-"+user.discriminator},
            "guild": user.guild.id
            }

        logger.info(log)

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

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        log = {
            "action": "on_guild_remove",
            "guild": {"id": guild.id, "name": guild.name}
        }

        logger.info(log) 

def setup(bot):
    bot.add_cog(Events(bot))