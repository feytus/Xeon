import datetime
import discord
import random
import string
import asyncio
import pyimgur
import os

from captcha.image import ImageCaptcha

from discord.ext import commands
from discord import ApplicationCommandInvokeError, Bot, ApplicationContext, Embed, Member, Guild, PermissionOverwrite, Message, ui

from utils.warning import Warning
from utils.color import Color
from utils.config import Config
from utils.database import Database
from utils.logs import logger

class ReportView(ui.View):
    def __init__(self, error_dict: dict):
        super().__init__(timeout=30)
        self.error_dict = error_dict
        
    @ui.button(
        label="Report bug",
        style=discord.ButtonStyle.grey,
        custom_id="report_view:report_bug",
    )
    async def report(self, button: discord.ui.Button, interaction: discord.Interaction):        
        Database.report_bug(self.error_dict)
        embed = Embed(title="Report bug", description=":white_check_mark: The **bug has been reported**, we will make sure to **fix it as soon as possible**.", color=Color.get_color("lite"))
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
class Events(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.warning = Warning()
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
        
        logger.info(f"Logged in as {self.bot.user} (ID: {self.bot.user.id})")
        logger.info(msg="latency : " + str(round(self.bot.latency * 1000)) + " ms")

        for guild in self.bot.guilds:
            if not Database.check_config(guild.id):
                if not Config.is_config(guild):
                    Config.config_server(guild)
                    logger.info({"action": "configuration", "guild": {"id": guild.id, "name": guild.name}})
            else:
                if not Database.check_guild_config(guild.id):
                    Database.create_guild_collection(guild.id)
                    logger.info({"action": "configuration", "guild": {"id": guild.id, "name": guild.name}})

        log = {"action": "on_ready"}

        logger.info(log)

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: ApplicationContext, error):
        error_dict = {
            "name": ctx.command.name,
            "options": [{key: value for key, value in options.items() if key != "type"} for options in ctx.selected_options] if ctx.selected_options is not None else None,
            "author_id": ctx.author.id,
            "guild_id": ctx.guild.id,
            "error": str(error),
            "date": datetime.datetime.now().timestamp()
        }
        
        view = ReportView(error_dict)
        
        if isinstance(error, ApplicationCommandInvokeError):
            if not Database.check_config(ctx.guild.id):
                await ctx.respond(
                    embed=Embed(
                        title="Error",
                        description="The bot is still in **BETA version so it may have bugs**.",
                        color=Color.get_color("sanction"),
                        timestamp=datetime.datetime.utcnow()
                    ),
                    view=view,
                    ephemeral=True,
                    delete_after=10
                )
            else:
                await ctx.respond(
                    embed=Embed(
                        title="Error",
                        description="The bot is still in **BETA version so it may have bugs**. Thank you for the **report by clicking on the button**.",
                        color=Color.get_color("sanction"),
                        timestamp=datetime.datetime.utcnow()
                    ),
                    view=view,
                    ephemeral=True,
                    delete_after=10
                )
        else:
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

    @commands.Cog.listener()
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
        guild = user.guild

        if not Database.check_config(user.guild.id):
            role_id = Config.get_config(guild.id, "default_role")
        else:
            role_id  = Database.get_config(guild.id).get("default_role")

        default_role = guild.get_role(role_id)

        if default_role is None:
            return False

        if len(os.listdir(f"data/{guild.id}/captcha/")) >= 10:
            for file in os.listdir(f"data/{guild.id}/captcha/"):
                os.remove(f"data/{guild.id}/captcha/{file}")

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

        embed = Embed(title="Captcha", description=f"{user.mention} Please send **the code**", color=discord.Color.random())
        embed.set_image(url=uploaded_image.link)
        message_captcha = await channel.send(embed=embed)

        try:
            response: Message = await self.bot.wait_for("message", check=lambda response: response.author == user, timeout=30)
        except asyncio.TimeoutError:
            await user.kick(reason="Captcha timeout")
            await channel.delete()
            return False
        

        if response.content == result_str:
            await user.add_roles(default_role)
            await message_captcha.delete()
            await response.delete()

        else:
            await user.kick(reason="Captcha failed")
            await message_captcha.delete()
            await response.delete()

        await channel.delete()

    @commands.Cog.listener()
    async def on_member_join(self, user: Member):
        if not Database.check_config(user.guild.id):
            self.warning.new_member(user, user.guild.id)

        if user.guild.system_channel is not None:
            embed = Embed(title=f"Welcome {user} !",
                            description=f"**{user.mention} joined the server !**", color=Color.get_color("lite"))
            embed.set_author(name=user.guild.name, icon_url=user.guild.icon)
            embed.set_thumbnail(url=user.display_avatar)
            embed.timestamp = user.joined_at

            await user.guild.system_channel.send(embed=embed)

        if Database.check_config(user.guild.id):
            if Database.get_config(user.guild.id).get("default_role") is not None:
                await self.captcha_check(user)

        log = {
            "action": "on_member_join", 
            "user": {"id": user.id, "name": user.name+"-"+user.discriminator},
            "guild": user.guild.id
            }

        logger.info(log)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: Guild):
        if not Database.check_config(guild.id):
            if not Config.is_config(guild):
                Config.config_server(guild)
                logger.info({"action": "configuration", "guild": {"id": guild.id, "name": guild.name}})
        else:
            if not Database.check_guild_config(guild.id):
                Database.create_guild_collection(guild.id)
                logger.info({"action": "configuration", "guild": {"id": guild.id, "name": guild.name}})
            
        log = {
            "action": "on_guild_join",
            "guild": {"id": guild.id, "name": guild.name},
            "is configured": (Config.is_config(guild) or Database.check_guild_config(guild.id))
        }

        logger.info(log)  

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: Guild):
        if Database.check_config(guild.id):
            Database.delete_guild(guild.id)

        log = {
            "action": "on_guild_remove",
            "guild": {"id": guild.id, "name": guild.name}
        }

        logger.info(log) 

def setup(bot):
    bot.add_cog(Events(bot))