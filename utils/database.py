import os

from pprint import pprint
from pymongo import MongoClient

from dotenv import load_dotenv
from random import randint
from datetime import datetime

load_dotenv()


username = os.getenv('MONGO_USERNAME')
password = os.getenv("MONGO_PWD")

connection_string = f"mongodb+srv://{username}:{password}@xeon.1p6bw.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(connection_string)

guild_db = client["guilds"]

class Database:
    def check_config(guild_id: int):
        try:
            client.server_info()
        except:
            return False

        return True
    
    def check_guild_config(guild_id: int):
        if guild_db[str(guild_id)] is None:
            return False

        return True

    def create_guild_collection(guild_id: int):
        guild_db.create_collection(str(guild_id))

    def insert_config(guild_id: int, element, value):
        collection = guild_db[str(guild_id)]

        guild_config_document = {
            "type": "config",
            element: value
        }

        collection.insert_one(guild_config_document)


    def get_config(guild_id: int):
        collection = guild_db[str(guild_id)]
        guild_data_document = collection.find_one({"type": "config"})

        if guild_data_document is None:
            guild_data_document = {}

        return guild_data_document

    def update_config(guild_id: int, element, value):
        collection = guild_db[str(guild_id)]

        if collection.find_one({"type": "config"}) is None:
            guild_config_document = {
            "type": "config",
            element: value
            }

            collection.insert_one(guild_config_document)
            return

        all_updates = {
            "$set": {
                element: value,
            }
        }

        collection.update_one({"type": "config"}, all_updates)

    def add_warnings(guild_id: int, user_id: int, reason, author_id: int):
        collection = guild_db[str(guild_id)]

        guild_warning_document = {
            "reason": reason,
            "author_id": author_id,
            "date": datetime.now().timestamp(),
            "id": randint(0, 1000000)
        }
        
        docs = list(collection.find({"user_id": user_id}))

        if len(docs) == 0:
            collection.insert_one(
                {
                "type": "user",
                "user_id": user_id
                }
            )
        
        collection.update_one(
            {"user_id": user_id},
            {"$addToSet": {"warnings": guild_warning_document}}
            )

    def get_warnings(guild_id: int, user_id: int):
        collection = guild_db[str(guild_id)]
        guild_data_document = list(collection.find({"user_id": user_id}))

        warnings = []

        if guild_data_document == []:
            return warnings

        warnings = [waring for waring in guild_data_document[0].get("warnings")]

        return warnings

    def remove_warning(guild_id: int, user_id: int, warning_id: int):
        collection = guild_db[str(guild_id)]

        collection.update_one(
            {"user_id": user_id},
            {"$pull": {"warnings": {"id": warning_id} if warning_id is not None else {}}} 
        )


    def delete_guild(guid_id: int):
        collection = guild_db[str(guid_id)]
        collection.drop()
        
    def report_bug(error_dict: dict):
        collection = guild_db["bugs"]
        
        collection.insert_one(error_dict)

