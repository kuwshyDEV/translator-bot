import discord
import discord.ext
from discord.ext import commands

import os
from dotenv import load_dotenv

import asyncio

load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')
APPLICATION_ID = os.getenv('DISCORD_APPLICATION_ID')

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
client = commands.Bot(intents=intents, command_prefix='.', application_id=APPLICATION_ID)

owner_id = 1032029100468076624

@client.event
async def on_ready():
    await client.tree.sync()
    print("ready")

async def load_cogs():
    print('Loading cogs...')
    base_path = 'Python Projects/Translator Bot/cogs'
    for root, _, files in os.walk(base_path):
        for filename in files:
            if filename.endswith('.py'):
                rel_path = os.path.relpath(root, base_path)
                if rel_path == ".":
                    module_name = f"{filename[:-3]}"
                else:
                    module_name = f"{rel_path}.{filename[:-3]}"
                module_name = module_name.replace(os.sep, '.')
                try:
                    await client.load_extension(f"cogs.{module_name}")
                    print(f'Loaded cogs.{module_name}')
                except Exception as e:
                    print(f'Failed to load cogs.{module_name}: {e}')
    print('Cogs loaded.')


async def main():
    await load_cogs()
    await client.start(TOKEN)
    await client.tree.sync()

if __name__ == "__main__":
    if TOKEN and APPLICATION_ID:
        asyncio.run(main())
    else:
        print("Error: Bot token or application ID not found. Please add them to the .env file.")