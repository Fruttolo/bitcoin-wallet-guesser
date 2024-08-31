import discord
import os
from dotenv import load_dotenv
from guess import Guesser
from check import Checker
import sys
import asyncio
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Get the environment variable
TOKEN = os.getenv('DISCORD_TOKEN')
STORAGE_DB = os.getenv('STORAGE_DB')
CHANNEL = int(os.getenv('CHANNEL'))

# Create an instance of a Client. This is the connection to Discord.
intents = discord.Intents.default()
intents.guilds = True
intents.guild_messages = True
client = discord.Client(intents=intents)

# Send a message to the first text channel of the first guild
async def send_message(message):
    await client.guilds[0].text_channels[CHANNEL].send(message)

def write_log(message):
    with open("log.txt", "a") as log_file:
        log_file.write(message + "\n")

# Gestione delle ecccezioni
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    while True:
        try:
            if bot_type == "GUESSER":
                bot = Guesser(STORAGE_DB)
                await send_message(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Guesser started")
                print( datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " - Guesser started")
                bot.run()
            elif bot_type == "CHECKER":
                bot = Checker(STORAGE_DB)
                await send_message(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Checker started")
                print( datetime.now().strftime("%Y-%m-%d %H:%M:%S"), " - Checker started")
                bot.run()
        except Exception as e:
            print(bot_type + " - An exception occurred: " + str(e))
            write_log( datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - " + bot_type + " - An exception occurred: " + str(e))
            await send_message( datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - " + bot_type + " - An exception occurred: " + str(e))
            await asyncio.sleep(60*3)

print("Select the bot to start:")
print("1. Checker")
print("2. Guesser")

if len(sys.argv) >= 2:
    choice = sys.argv[1]
else:
    choice = input("Enter your choice (1 or 2): ")

while choice != "1" and choice != "2":
    print("Invalid choice. Please enter 1 or 2.")
    choice = input("Enter your choice (1 or 2): ")

if choice == "1":
    bot_type = "CHECKER"
elif choice == "2":
    bot_type = "GUESSER"

# Run the bot
client.run(TOKEN)

