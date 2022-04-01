import os
import json

from discord import Bot, Guild, Member

class Warning:
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    def new_member(self, user: Member, guild: Guild):
        with open(f'data/{guild.id}/warnings.json', 'r') as file:
            data = json.load(file)
            if str(user.id) not in data.keys():
                data[user.id] = {'warnings': []}
            file.close()

        with open(f'data/{guild.id}/warnings.json', 'w') as file:
            json.dump(data, file, indent=4)
            file.close()
        
    def new_warn(self, user: Member, guild: Guild, author: Member, reason: str):
        with open(f'data/{guild.id}/warnings.json', 'r') as file:
            data = json.load(file)
            warnings: list = data[str(user.id)]['warnings']
            warn = {"author": author.id, "reason": reason}
            warnings.append(warn)
            file.close()

        with open(f'data/{guild.id}/warnings.json', 'w') as file:
            json.dump(data, file, indent=4)
            file.close()

    def get_warnings(self, guild: Guild, user: Member):
        with open(f'data/{guild.id}/warnings.json', 'r') as file:
            data = json.load(file)
            warnings: list = data[str(user.id)]['warnings']
            file.close()
            return warnings

    def remove_warning(self, guild: Guild, user: Member, warning_index=None):
        with open(f'data/{guild.id}/warnings.json', 'r') as file:
            data = json.load(file)
            warnings: list = data[str(user.id)]['warnings']
            if warning_index is not None:
                warnings.pop(warning_index-1)
            else:
                warnings = []
            file.close()

        with open(f'data/{guild.id}/warnings.json', 'w') as file:
            json.dump(data, file, indent=4)
            file.close()

