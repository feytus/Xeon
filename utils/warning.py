import json

from datetime import datetime
from random import randint


class Warning:
    def new_member(self, user_id: int, guild_id: int):
        with open(f'data/{guild_id}/warnings.json', 'r') as file:
            data = json.load(file)
            if str(user_id) not in data.keys():
                data[user_id] = {'warnings': []}
            file.close()

        with open(f'data/{guild_id}/warnings.json', 'w') as file:
            json.dump(data, file, indent=4)
            file.close()
        
    def new_warn(self, user_id: int, guild_id: int, author_id: int, reason: str):
        with open(f'data/{guild_id}/warnings.json', 'r') as file:
            data = json.load(file)
            warnings: list = data[str(user_id)]['warnings']
            warn = {
                "reason": reason,
                "author_id": author_id,
                "date": datetime.now().timestamp(),
                "id": randint(0, 1000000)
            }

            warnings.append(warn)
            file.close()

        with open(f'data/{guild_id}/warnings.json', 'w') as file:
            json.dump(data, file, indent=4)
            file.close()

    def get_warnings(self, guild_id: int, user_id: int):
        with open(f'data/{guild_id}/warnings.json', 'r') as file:
            data = json.load(file)
            warnings: list = data[str(user_id)]['warnings']
            file.close()
            return warnings

    def remove_warning(self, guild_id: int, user_id: int, warning_id=None):
        with open(f'data/{guild_id}/warnings.json', 'r') as file:
            data = json.load(file)
            warnings: list = data[str(user_id)]['warnings']

            if warning_id is not None:
                for warning in warnings:
                    if warning['id'] == warning_id:
                        warnings.remove(warning)
            else:
                warnings = []

            file.close()

        with open(f'data/{guild_id}/warnings.json', 'w') as file:
            json.dump(data, file, indent=4)
            file.close()
