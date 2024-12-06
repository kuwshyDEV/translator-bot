import discord
from discord.ext import commands
from discord import app_commands
from googletrans import Translator, LANGUAGES
import json
import os

config_json_path = "Python Projects/Translator Bot/Database/config.json"

# Load config.json
def load_config():
    if os.path.exists(config_json_path):
        with open(config_json_path, "r") as f:
            return json.load(f)
    return {"auto_translate": {}}

# Save config.json
def save_config(config):
    with open(config_json_path, "w") as f:
        json.dump(config, f, indent=4)

class AutoTranslateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator()
        self.config = load_config()

    @app_commands.command(name="auto-translate", description="Enable auto-translation in a channel to a target language.")
    async def auto_translate(self, interaction: discord.Interaction, channel: discord.TextChannel, target_lang: str):
        target_lang = target_lang.lower()
        
        if target_lang not in LANGUAGES:
            await interaction.response.send_message("Invalid language code. Please use a valid ISO language code.", ephemeral=True)
            return

        # Update config with new channel and target language
        self.config["auto_translate"][str(channel.id)] = target_lang
        save_config(self.config)

        await interaction.response.send_message(f"Auto-translation enabled for {channel.mention} to `{LANGUAGES[target_lang]}`.")

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore bot messages and check if channel is set for auto-translation
        if message.author.bot or str(message.channel.id) not in self.config["auto_translate"]:
            return

        # Get target language and translate message
        target_lang = self.config["auto_translate"][str(message.channel.id)]
        try:
            translated = self.translator.translate(message.content, dest=target_lang)
            translated_text = translated.text

            # Delete the original message
            await message.delete()

            # Send the translated message mentioning the author
            await message.channel.send(f"{message.author.mention}: {translated_text}")
        
        except Exception as e:
            print(f"Translation error: {e}")
            await message.channel.send("There was an error translating the message.", delete_after=5)

async def setup(bot):
    await bot.add_cog(AutoTranslateCog(bot))
