from genericpath import isfile
import os

# Installation of the package(s)
packages = ['requests']
[os.system(f'pip install {package}') for package in packages]
os.system('cls')
if not isfile('.env'):
    token = input("Enter the token of your bot : ")
    client_id = input("Enter your client_id | Enter 'None' if you don't want : ")
    acces_token = input("Enter your acces_token | Enter 'None' if you don't want : ")
    with open('.env', 'a') as file:
        file.write(f'token="{token}"\nclient_id="{client_id}"\nacces_token="{acces_token}"')
        file.close()