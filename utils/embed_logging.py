import datetime

from discord import Bot, Member, User
from discord import TextChannel
from discord import Embed
from discord.embeds import EmbedProxy

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
            "proof": data.get("proof"),
            "channel": data.get("channel"),
            "element": data.get("element"),
            "value": data.get("value"),
        }
        
        author: User = self.bot.get_user(embed_data.get("author"))
        action = embed_data.get("action")
        user: User = self.bot.get_user(embed_data.get("user"))
        channel = embed_data.get("channel")

        embed = Embed(timestamp=datetime.datetime.utcnow())
        embed.set_footer(text=author.id, icon_url=author.display_avatar)
        
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

        #embed.set_thumbnail(author.display_avatar)

        if action == "ban":
            embed.description = f"**user.mention has been banned from the server**"
            embed.color = Color.get_color("sanction")
            embed.add_field(name="Moderator", value=author.mention)

        elif action == "clear":
            embed.description = f"**author.mention has cleared the channel <#{channel}>**"
            embed.color = Color.get_color("lite")
            embed.add_field(name="Moderator", value=author.mention)

        elif action == "kick":
            embed.description = f"**user.mention has been kicked from the server**"
            embed.color = Color.get_color("sanction")
            embed.add_field(name="Moderator", value=author.mention)
        
        elif action == "remove_warning":
            embed.description = f"**author.mention has removed a warning to {user}**"
            embed.color = Color.get_color("lite")
            embed.add_field(name="Moderator", value=author.mention)

        elif action == "tempban":
            embed.description = f"**user.mention has been temporarily banned from the server**"
            embed.color = Color.get_color("sanction")
            embed.add_field(name="Moderator", value=author.mention)

        elif action == "timeout":
            embed.description = f"**user.mention has been timed out**"
            embed.color = Color.get_color("sanction")
            embed.add_field(name="Moderator", value=author.mention)

        elif action == "warn":
            embed.description = f"**user.mention has been warned**"
            embed.color = Color.get_color("sanction")
            embed.add_field(name="Moderator", value=author.mention)

        elif action == "unban":
            embed.description = f"**user.mention has been unbanned from the server**"
            embed.color = Color.get_color("lite")
            embed.add_field(name="Moderator", value=author.mention)
        
        elif action == "report":
            embed.description = f"**user.mention has been reported**"
            embed.color = Color.get_color("sanction")
            embed.add_field(name="Author", value=author.mention)

        elif action == "server_config":
            embed.description = f"**author.mention has changed the server configuration**"
            embed.color = Color.get_color("lite")
            embed.add_field(name="Moderator", value=author.mention)

        return embed    