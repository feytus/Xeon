import datetime
import asyncio
import logging

from discord.ext import commands
from discord.commands import slash_command
from discord import ApplicationContext, Message, Option, Bot, Embed
from discord.abc import GuildChannel
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
    async def config_server(self, ctx: ApplicationContext, item: Option(str, description="The item to config", choices=["logging channel", "report channel", "default role"])):
        await ctx.defer(ephemeral=True)

        embed = Embed(title="Configuration", color=Color.get_color("lite"), timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=ctx.guild.icon)

        if item in ("logging channel", "report channel"):
            embed.description=f"**Enter the ID of the {item}**"
        elif item == "default role":
            embed.description=f"**Enter the ID of the {item}**"

        message = await ctx.respond(embed=embed, ephemeral=True)

        try:
            response: Message = await self.bot.wait_for("message", check=lambda response: response.author == ctx.author, timeout=30)
        except asyncio.TimeoutError:
            embed.description = "**You didn't enter a value in time**"
            await message.edit(embed=embed)
        
        value = response.content
        if value.isdigit():
            if item in ("logging channel", "report channel"):
                guild_channel = self.bot.get_channel(int(value))

                if guild_channel is None:
                    embed.description = "**The channel doesn't exist**"
                    await message.edit(embed=embed)
                    await response.delete()

                    return False

                item_value = guild_channel

            elif item == "default role":
                default_role = ctx.guild.get_role(int(value))

                if default_role is None:
                    embed.description = "**The role doesn't exist**"
                    await message.edit(embed=embed)
                    await response.delete()

                    return False

                item_value = default_role
        else:
            embed.description = "**The value isn't an ID**"
            await message.edit(embed=embed)
            await response.delete()
            return False

        if item == "logging channel":
            element = "logging_channel"
        elif item == "report channel":
            element = "report_channel"
        elif item == "default role":
            element = "default_role"

        self.config.config_element(ctx.guild, element=element, value=int(value))

        config = self.config.get_config(ctx.guild)
        logging_channel = config.get("logging_channel")
        report_channel = config.get("report_channel")
        default_role = config.get("default_role")

        embed=Embed(
            title="Configuration", 
            description=f"**The {item} has been set to {item_value.mention}**", 
            color=Color.get_color("lite"), 
            timestamp=datetime.datetime.utcnow())
        embed.set_thumbnail(url=ctx.guild.icon)

        if logging_channel is not None:
            embed.add_field(name="Logging channel", value=f"<#{logging_channel}>", inline=False)
        if report_channel is not None:
            embed.add_field(name="Report channel", value=f"<#{report_channel}>", inline=False)
        if default_role is not None:
            embed.add_field(name="Default role", value=f"<@&{default_role}>", inline=False)

        await message.edit(embed=embed)
        await response.delete()

        channel_logging = self.bot.get_channel(
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
            "author": {"id": ctx.user.id, "name": ctx.user.name+"#"+ctx.user.discriminator},
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
        embed.set_thumbnail(url=ctx.guild.icon)

        self.config.get_config(ctx.guild)

        config = self.config.get_config(ctx.guild)
        logging_channel = config.get("logging_channel")
        report_channel = config.get("report_channel")
        default_role = config.get("default_role")

        if logging_channel is not None:
            embed.add_field(name="Logging channel", value=f"<#{logging_channel}>", inline=False)
        if report_channel is not None:
            embed.add_field(name="Report channel", value=f"<#{report_channel}>", inline=False)
        if default_role is not None:
            embed.add_field(name="Default role", value=f"<@&{default_role}>", inline=False)


        log = {
            "action": "get_config", 
            "author": {"id": ctx.user.id, "name": ctx.user.name+"#"+ctx.user.discriminator},
            "guild": {"id": ctx.guild.id, "name": ctx.guild.name}
            }

        logger.info(log)

        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(Server_Config(bot))