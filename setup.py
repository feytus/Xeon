from genericpath import isfile
import os

packages = [module for module in open('requirements.txt').read().split('\n') if module]

[os.system(f'pip install {package}') for package in packages]
os.system('cls')

if not isfile('.env'):
    TOKEN = input("Enter the token of your bot : ")
    MONGO_USERNAME = input("Enter your mongo username : | Enter 'None' if you don't want : ")
    MONGO_PWD = input("Enter your mongo password : | Enter 'None' if you don't want : ")
    CLIENT_ID = input("Enter your CLIENT_ID from twitch.tv | Enter 'None' if you don't want : ")
    CLIENT_SECRET = input("Enter your CLIENT_SECRET from twitch.tv | Enter 'None' if you don't want : ")
    IMGUR_CLIENT_ID = input("Enter your CLIENT_ID from imgur.com | Enter 'None' if you don't want : ")

    with open('.env', 'a') as file:
        file.write(f'TOKEN="{TOKEN}"\nCLIENT_ID="{CLIENT_ID}"\nCLIENT_SECRET="{CLIENT_SECRET}"\nIMGUR_CLIENT_ID="{IMGUR_CLIENT_ID}\nMONGO_USERNAME="{MONGO_USERNAME}"\nMONGO_PWD="{MONGO_PWD}"')
        file.close()
else:
    print("The bot is already configured | delete .env file if you want to configure it again")

