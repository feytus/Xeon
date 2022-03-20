from discord.commands import SlashCommand
from random import randint
from datetime import timedelta
from discord import SelectOption


all_commands = {
            "timeout": {"description": "Timeout a member of the discord", "utilisation": "/timeout [user] [duration] [time] [*reason]"},
            "user_info": {"description": "Get some informations about a member of the discord", "utilisation": "/user_info [*user]"},
            "ban": {"description": "Ban a member of the discord", "utilisation": "/ban [user] [*reason]"},
            "clear": {"description": "Clear the channel", "utilisation": "/clear [*amount]"},
            "kick": {"description": "Kick a member of the discord", "utilisation": "/kick [user] [*reason]"},
            "tempban": {"description": "Temporarily ban member of the discord", "utilisation": "/tempban [user] [duration] [time] [*reason]"},
            "twitch_info": {"description": "Get some informations about a twitch channel", "utilisation": "/twitch_info [twitch_channel]"},
            "ban_list": {"description": "Get a list of all banned members", "utilisation": "/ban_list"},
            "warn": {"description": "Warn a member of the discord", "utilisation": "/warn [user] [reason]"},
            "warnings": {"description": "Get a list of warnings from a member of the discord", "utilisation": "/warnings [user]"},
            "remove_warning": {"description": "Remove a warning from a member of the discord", "utilisation": "/remove_warning [user] [warning_number]"},
            }

command = [SelectOption(label=command[0], description=command[1]['description']) for command in all_commands.items()]

def get_color(colors: list):
    return colors[randint(0, len(colors)-1)]

def time_to_second(time, duration):
    duration = int(duration)
    if time == "second":
        date = timedelta(seconds=duration)
    elif time == "minute":
        date = timedelta(minutes=duration)
    elif time == "hour":
        date = timedelta(hours=duration)
    elif time == "day":
        date = timedelta(days=duration)
    elif time == "week":
        date = timedelta(days=duration*7)
    elif time == "month":
        date = timedelta(days=duration*30)
    return date