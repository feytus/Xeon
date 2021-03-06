import json
import os

from discord import Bot, Guild

class Config:
    def config_element(guild: Guild, element: str, value: str):
        if not Config.is_config(guild):
            Config.config_server(guild)

        with open(f'data/{guild.id}/config.json', 'r') as file:
            config: dict = json.loads(file.read())
            file.close()

        config[element] = value

        with open(f'data/{guild.id}/config.json', 'w') as file:
            file.write(json.dumps(config, indent=5))
            file.close()

    def config_server(guild: Guild):
        if not os.path.exists(f'data/'):
            os.mkdir('data')
        
        if not os.path.exists(f'data/{guild.id}'):
            os.mkdir(f'data/{guild.id}')

        if not os.path.exists(f'data/{guild.id}/captcha'):
            os.mkdir(f'data/{guild.id}/captcha')

        if not Config.is_config(guild, "WARNINGS_FILE"):
            with open(f'data/{guild.id}/warnings.json', 'w') as file:
                file.write("{}")
                file.close()
        
        if not Config.is_config(guild, "CONFIG_FILE"):
            with open(f'data/{guild.id}/config.json', 'w') as file:
                file.write("{}")
                file.close()
                
    def is_config(guild: Guild, element: str=None):
        elements = {
            "GUILD_FOLDER": f'data/{guild.id}',
            "CAPTCHA_FOLDER": f'data/{guild.id}/CAPTCHA',
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
    
    def get_config(guild: Guild, element: str=None):
        with open(f'data/{guild.id}/config.json', 'r') as file:
            config: dict = json.loads(file.read())
            file.close()

        if element is not None:
            return config.get(element)
            
        return config
        
            

        