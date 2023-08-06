import discord
from discord.ext import commands
from discord import app_commands
from messageformater import helper

class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="help", description="See a list of all MunchieBots commands")
    async def help_message(self, interaction: discord.Integration):
        helpMessage = helper()
        await interaction.response.send_message(embed=helpMessage, ephemeral=True)
        
async def setup(bot:commands.Bot) ->None:
    await bot.add_cog(HelpCog(bot))