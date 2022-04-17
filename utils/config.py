import json
import os

from discord import Bot, Guild

class Config:
    def __init__(self, bot: Bot):
        self.bot: Bot = bot

    def config_element(self, guild: Guild, element: str, value: str):
        if not self.is_config(guild):
            self.config_server(guild)

        with open(f'data/{guild.id}/config.json', 'r') as file:
            config: dict = json.loads(file.read())
            file.close()

        config[element] = value

        with open(f'data/{guild.id}/config.json', 'w') as file:
            file.write(json.dumps(config, indent=5))
            file.close()

    def config_server(self, guild: Guild):
        if not os.path.exists(f'data/'):
            os.mkdir('data')
        
        if not os.path.exists(f'data/{guild.id}'):
            os.mkdir(f'data/{guild.id}')

        with open(f'data/{guild.id}/warnings.json', 'a') as file:
            file.write('{}')
            file.close()

        with open(f'data/{guild.id}/config.json', 'a') as file:
            file.write('{}')
            file.close()

    def is_config(self, guild: Guild, element: str=None):
        elements = {
            "FOLDER": f'data/{guild.id}',
            "CONFIG_FILE": f'data/{guild.id}/config.json',
            "WARNINGS_FILE": f'data/{guild.id}/warnings.json'
        }

        if element in elements.keys():
            return os.path.exists(element)

        for key in elements.keys():
            if not os.path.exists(elements[key]):
                return False

        with open(f'data/{guild.id}/config.json', 'r') as file:
            config = file.read()
            file.close()
            if config == "":
                return False
        
        with open(f'data/{guild.id}/warnings.json', 'r') as file:
            config = file.read()
            file.close()
            if config == "":
                return False
                
        return True
    
    def get_config(self, guild: Guild):
        with open(f'data/{guild.id}/config.json', 'r') as file:
            config: dict = json.loads(file.read())
            file.close()

        return config

        