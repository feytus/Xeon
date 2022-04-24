import datetime
import asyncio
import logging

from discord.ext import commands
from discord.commands import slash_command
from discord import ApplicationContext, Message, Option, Bot, Embed
from discord.ext.commands import bot_has_permissions, has_permissions

from utils.color import Color
from utils.logs import logger
from utils.config import Config
from utils.embed_logging import EmbedLogging

guilds=[809410416685219853, 803981117069852672]

class Server_Config(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.config = Config(bot)
        self.embed_logging = EmbedLogging(bot)

    @slash_command(name="config_server", description="Configure the bot for the discord", guild_ids=guilds)
    @has_permissions(administrator=True)
    @bot_has_permissions(send_messages=True, read_messages=True)
    async def config_server(self, ctx: ApplicationContext, channel: Option(str, description="The channel to config", choices=["logging channel", "report channel"])):
        await ctx.defer(ephemeral=True)

        embed = Embed(title="Configuration", description=f"**Enter the ID of the {channel}**", color=Color.get_color("lite"), timestamp=datetime.datetime.utcnow())
        message = await ctx.respond(embed=embed, ephemeral=True)

        try:
            response: Message = await self.bot.wait_for("message", check=lambda response: response.author == ctx.author, timeout=30)
        except asyncio.TimeoutError:
            embed.description = "**You didn't enter a value in time**"
            await message.edit(embed=embed)
        
        value = response.content
        if value.isdigit():
            guild_channel = self.bot.get_channel(int(value))
            if guild_channel is None:
                embed.description = "**The channel doesn't exist**"
                await message.edit(embed=embed)
                return False
        else:
            embed.description = "**The value isn't an ID**"
            await message.edit(embed=embed)

        if channel == "logging channel":
            element = "logging_channel"
        elif channel == "report channel":
            element = "report_channel"

        self.config.config_element(ctx.guild, element=element, value=value)

        config = self.config.get_config(ctx.guild)
        logging_channel = config.get("logging_channel")
        report_channel = config.get("report_channel")

        embed=Embed(
            title="Configuration", 
            description=f"**The {channel} has been set to {guild_channel.mention}**", 
            color=Color.get_color("lite"), 
            timestamp=datetime.datetime.utcnow())

        if logging_channel is not None:
            embed.add_field(name="Logging channel", value=f"<#{logging_channel}>", inline=False)
        if report_channel is not None:
            embed.add_field(name="Report channel", value=f"<#{report_channel}>", inline=False)

        await message.edit(embed=embed)
        await response.delete()

        channel_logging = await self.bot.fetch_channel(
            self.config.get_config(ctx.guild).get("logging_channel")
        )

        if channel_logging is not None:
            embed_logging = self.embed_logging.get_embed(
                data={
                    "action": "config_server",
                    "author": ctx.user.id,
                    "element": element,
                    "value": guild_channel,
                }
            )
            await channel_logging.send(embed=embed_logging)

        log = {
            "action": "config_server", 
            "author": {"id": ctx.user.id, "name": ctx.user.display_name+"#"+ctx.user.discriminator},
            "element": element,
            "value": value,
            "guild": {"id": ctx.guild.id, "name": ctx.guild.name}
            }

        logger.info(log)

    @slash_command(name="get_config", description="Get the configuration of the bot for the server", guild_ids=guilds)
    @has_permissions(administrator=True)
    @bot_has_permissions(send_messages=True, read_messages=True)
    async def get_config(self, ctx: ApplicationContext):
        await ctx.defer(ephemeral=True)

        embed=Embed(
            title="Configuration", 
            description=f"**Get the configuration of the bot for the server**", 
            color=Color.get_color("lite"), 
            timestamp=datetime.datetime.utcnow())

        self.config.get_config(ctx.guild)

        config = self.config.get_config(ctx.guild)
        logging_channel = config.get("logging_channel")
        report_channel = config.get("report_channel")

        if logging_channel is not None:
            embed.add_field(name="Logging channel", value=f"<#{logging_channel}>", inline=False)
        if report_channel is not None:
            embed.add_field(name="Report channel", value=f"<#{report_channel}>", inline=False)


        log = {
            "action": "get_config", 
            "author": {"id": ctx.user.id, "name": ctx.user.display_name+"#"+ctx.user.discriminator},
            "guild": {"id": ctx.guild.id, "name": ctx.guild.name}
            }

        logger.info(log)

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Server_Config(bot))