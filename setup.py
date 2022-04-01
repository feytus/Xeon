from genericpath import isfile
import os

packages = [module for module in open('requirements.txt').read().split('\n') if module]

[os.system(f'pip install {package}') for package in packages]
os.system('cls')

if not isfile('.env'):
    token = input("Enter the token of your bot : ")
    client_id = input("Enter your client_id | Enter 'None' if you don't want : ")
    client_secret = input("Enter your client_secret | Enter 'None' if you don't want : ")
    with open('.env', 'a') as file:
        file.write(f'token="{token}"\nclient_id="{client_id}"\client_secret="{client_secret}"')
        file.close()
else:
    print("The bot is already configured | delete .env file if you want to configure it again")

