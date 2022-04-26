from genericpath import isfile
import os

packages = [module for module in open('requirements.txt').read().split('\n') if module]

[os.system(f'pip install {package}') for package in packages]
os.system('cls')

if not isfile('.env'):
    TOKEN = input("Enter the token of your bot : ")
    CLIENT_ID = input("Enter your client_id | Enter 'None' if you don't want : ")
    CLIENT_SECRET = input("Enter your client_secret | Enter 'None' if you don't want : ")
    IMGUR_CLIENT_ID = input("Enter your client_id from IMGUR | Enter 'None' if you don't want : ")
    with open('.env', 'a') as file:
        file.write(f'TOKEN="{TOKEN}"\nCLIENT_ID="{CLIENT_ID}"\nCLIENT_SECRET="{CLIENT_SECRET}"\nIMGUR_CLIENT_ID="{IMGUR_CLIENT_ID}"')
        file.close()
else:
    print("The bot is already configured | delete .env file if you want to configure it again")

