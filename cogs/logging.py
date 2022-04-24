import datetime

from discord.ext import commands
from discord import Embed, Member, Message, Bot, TextChannel, VoiceChannel
from discord.abc import GuildChannel

from utils.color import Color
from utils.config import Config
from utils.logs import logger

class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        self.config = Config(bot)

    @commands.Cog.listener()
    async def on_member_update(self, before: Member, after: Member):
        logging_channel = await self.bot.fetch_channel(self.config.get_config(after.guild, "logging_channel"))

        embed_logging = Embed(title="Logging", description=f"**{after.mention} has updated his profile**", color=Color.get_color("lite"))
        embed_logging.set_thumbnail(url=after.display_avatar)
        embed_logging.timestamp = datetime.datetime.utcnow()

        before_roles = ""

        for role in before.roles:
            before_roles += f"{role.name}, "
        
        after_roles = ""

        for role in after.roles:
            after_roles += f"{role.name}, "

        info_before = {
            "nickname": before.nick,
            "roles": before_roles,
            "pending": before.pending,
        }

        info_after = {
            "nickname": after.nick,
            "roles": after_roles,
            "pending": after.pending,
        }

        for key in info_after.keys():
            if info_after[key] != info_before[key]:
                if key == "roles":
                    embed_logging.add_field(name=key, value=f"**{info_before[key]} :arrow_right: {info_after[key]}**", inline=True)
                else:
                    embed_logging.add_field(name=f"**{key.capitalize()}", value=f"{info_before[key]} :arrow_right: {info_after[key]}**", inline=False)

        if logging_channel is not None and len(embed_logging.fields) > 0:
            await logging_channel.send(embed=embed_logging)

        log = {"action": "on_member_update", "user": after.id, "guild": after.guild.id}
        logger.info(log)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel: GuildChannel):
        logging_channel = await self.bot.fetch_channel(self.config.
        get_config(channel.guild, "logging_channel"))
        embed_logging = Embed(title="Logging", description=f"**The channel {channel.mention} has been deleted**", color=Color.get_color("lite"))
        embed_logging.set_thumbnail(url=channel.guild.icon)
        embed_logging.timestamp = datetime.datetime.utcnow()

        if logging_channel is not None:
            await logging_channel.send(embed=embed_logging)

        log = {"action": "on_guild_channel_delete", "channel": channel.id}
        logger.info(log)

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel: GuildChannel):
        logging_channel = await self.bot.fetch_channel(self.config.get_config(channel.guild, "logging_channel"))

        embed_logging = Embed(title="Logging", description=f"**The channel {channel.mention} has been created**", color=Color.get_color("lite"))
        embed_logging.set_thumbnail(url=channel.guild.icon)
        embed_logging.timestamp = datetime.datetime.utcnow()

        if logging_channel is not None:
            await logging_channel.send(embed=embed_logging)

        log = {"action": "on_guild_channel_create", "channel": channel.id}
        logger.info(log)
    
    @commands.Cog.listener()
    async def on_guild_channel_update(self, before: GuildChannel, after: GuildChannel):
        logging_channel = await self.bot.fetch_channel(self.config.get_config(after.guild, "logging_channel"))

        embed_logging = Embed(title="Logging", description=f"**The channel {before.mention} has been edited**", color=Color.get_color("lite"))
        embed_logging.set_thumbnail(url=before.guild.icon)

        if before.name != after.name:
            embed_logging.add_field(name="Name", value=f"**{before.name} :arrow_right: {after.name}**", inline=False)
        if before.position != after.position:
            embed_logging.add_field(name="Position", value=f"**{before.position} :arrow_right: {after.position}**", inline=False)

        if after is TextChannel:
            before: TextChannel = before
            after: TextChannel = after
            
            if before.news != after.news:
                embed_logging.add_field(name="News", value=f"**{before.news} :arrow_right: {after.news}**", inline=False)
            if before.category != after.category:
                embed_logging.add_field(name="Category", value=f"**{before.category_id} :arrow_right: {after.category_id}**", inline=False)
            if before.nsfw != after.nsfw:
                embed_logging.add_field(name="NSFW", value=f"**{before.nsfw} :arrow_right: {after.nsfw}**", inline=False)

        if after is VoiceChannel:
            before: VoiceChannel = before
            after: VoiceChannel = after

            if before.rtc_region != after.rtc_region:
                embed_logging.add_field(name="RTC Region", value=f"**{before.rtc_region} :arrow_right: {after.rtc_region}**", inline=False)
            if before.bitrate != after.bitrate:
                embed_logging.add_field(name="Bitrate", value=f"**{before.bitrate} :arrow_right: {after.bitrate}**", inline=False)
            if before.user_limit != after.user_limit:
                embed_logging.add_field(name="User Limit", value=f"**{before.user_limit} :arrow_right: {after.user_limit}**", inline=False)

        embed_logging.timestamp = datetime.datetime.utcnow()
        
        if logging_channel is not None:
            await logging_channel.send(embed=embed_logging)
        
        log = {"action": "on_guild_channel_update", "before": before, "after": after}
        logger.info(log)

    @commands.Cog.listener()
    async def on_message_edit(self, before: Message, after: Message):
        channel = await self.bot.fetch_channel(before.channel.id)

        if before.content == after.content:
            return False

        logging_channel = await self.bot.fetch_channel(self.config.get_config(channel.guild, "logging_channel"))

        embed_logging = Embed(title="Logging", description=f"**{before.author.mention} edited a message in {channel.mention}**", color=Color.get_color("lite"))
        embed_logging.add_field(name="Content", value=f"**{before.content} :arrow_right: {after.content}**", inline=False)

        embed_logging.set_thumbnail(url=before.author.display_avatar)
        embed_logging.set_footer(text=after.author.id, icon_url=after.author.display_avatar)
        embed_logging.timestamp = datetime.datetime.utcnow()
        
        if logging_channel is not None:
            await logging_channel.send(embed=embed_logging)

        log = {"action": "on_message_edit", "before": before.content, "after": after.content}
        logger.info(log)


def setup(bot):
    bot.add_cog(Logging(bot))
