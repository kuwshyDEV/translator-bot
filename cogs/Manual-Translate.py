import discord
from discord.ext import commands
from discord import app_commands, ui
from googletrans import Translator, LANGUAGES

class TranslateModal(ui.Modal, title="Translate Message"):
    source_language = ui.TextInput(label="Source Language (e.g., en, es)", placeholder="Enter source language code")
    target_language = ui.TextInput(label="Target Language (e.g., fr, de)", placeholder="Enter target language code")
    message = ui.TextInput(label="Message to Translate", style=discord.TextStyle.paragraph, placeholder="Enter your message here", required=True)

    def __init__(self, translator):
        super().__init__()
        self.translator = translator

    async def on_submit(self, interaction: discord.Interaction):
        source_lang = self.source_language.value.lower()
        target_lang = self.target_language.value.lower()
        text = self.message.value

        if source_lang not in LANGUAGES or target_lang not in LANGUAGES:
            await interaction.response.send_message("Invalid language code(s). Please use correct ISO language codes.", ephemeral=True)
            return
        
        try:
            translation = self.translator.translate(text, src=source_lang, dest=target_lang)
            translated_text = translation.text
            embed = discord.Embed(title="Translation", color=discord.Color.blue())
            embed.add_field(name="Original Message", value=text, inline=False)
            embed.add_field(name="Translated Message", value=translated_text, inline=False)
            embed.set_footer(text=f"{LANGUAGES[source_lang]} ➔ {LANGUAGES[target_lang]}")
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"Error: {e}", ephemeral=True)

class TranslateCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.translator = Translator()

    @app_commands.command(name="translate", description="Translate a message from any language to any language!")
    async def translate(self, interaction: discord.Interaction):
        modal = TranslateModal(translator=self.translator)
        await interaction.response.send_modal(modal)

async def setup(bot):
    await bot.add_cog(TranslateCog(bot))
