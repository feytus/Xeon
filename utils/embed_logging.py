import datetime

from discord import Bot, Member, User
from discord import TextChannel
from discord import Embed

from utils.color import Color


class EmbedLogging:
    def __init__(self, bot: Bot) -> None:
        self.channel: TextChannel = None
        self.bot = bot
        
    def is_logging_channel(self):
        if self.bot is not None:
            return self.bot.get_channel(self.channel.id) is not None

    def get_embed(self, data: dict):
        embed_data = {
            "action": data.get("action"),
            "user": data.get("user"),
            "author": data.get("author"),
            "duration": data.get("duration"),
            "time": data.get("time"),
            "amount": data.get("amount"),
            "warning": data.get("warning"),
            "reason": data.get("reason"),
            "channel": data.get("channel")
        }
        
        author: User = self.bot.get_user(embed_data.get("author"))
        action = embed_data.get("action")
        user: User = self.bot.get_user(embed_data.get("user"))
        channel = embed_data.get("channel")

        embed = Embed(timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=author.id, icon_url=author.display_avatar)
        embed.add_field(name="Moderator", value=author.mention)

        key_list = ["duration", "time", "author", "action", "channel", "user"]

        for key in embed_data.keys():
            value = embed_data[key]

            if (key == "duration" or key == "time") and value is not None:
                duration = embed_data.get("duration")
                time = embed_data.get("time")
                embed.add_field(name="Duration", value=f"{duration} {time}(s)")
            else:
                if key not in key_list and value is not None:
                    embed.add_field(name=key.capitalize(), value=value)

        embed.thumbnail = user.display_avatar

        if action == "ban":
            embed.description = f"**<@{user.id}> has been banned from the server**"
            embed.color = Color.get_color("sanction")

        elif action == "clear":
            embed.description = f"**<@{author.id}> has cleared the channel <#{channel}>**"
            embed.color = Color.get_color("lite")
            embed.thumbnail = author.display_avatar

        elif action == "kick":
            embed.description = f"**<@{user.id}> has been kicked from the server**"
            embed.color = Color.get_color("sanction")
        
        elif action == "remove_warning":
            embed.description = f"**<@{author.id}> has removed a warning to {user}**"
            embed.color = Color.get_color("lite")

        elif action == "tempban":
            embed.description = f"**<@{user.id}> has been temporarily banned from the server**"
            embed.color = Color.get_color("sanction")

        elif action == "timeout":
            embed.description = f"**<@{user.id}> has been timed out**"
            embed.color = Color.get_color("sanction")

        elif action == "warn":
            embed.description = f"**<@{user.id}> has been warned**"
            embed.color = Color.get_color("sanction")

        elif action == "unban":
            embed.description = f"**<@{user.id}> has been unbanned from the server**"
            embed.color = Color.get_color("lite")

        return embed    