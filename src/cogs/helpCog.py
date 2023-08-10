import discord
from discord.ext import commands
from discord import app_commands

class HelpCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="help", description="See a list of all MunchieBots commands")
    async def help_message(self, interaction: discord.Integration):
        commandList = discord.Embed(
        colour = discord.Colour.dark_purple(),
        title = "Commands",
        )
        commandList.set_author(name="Munchie Bot >^.^<")
        commandList.add_field(name="/help", value="See list of commands.", inline=False)
        commandList.add_field(name="/global", value="@everyone to notify the whole server.", inline=False)
        commandList.add_field(name="/freegame", value="See the latest free game on epic.", inline=False)
        commandList.add_field(name="/ilovemunchie", value="Tell Munchie how you feel about her.", inline=False)
        await interaction.response.send_message(embed=commandList, ephemeral=True)
        
async def setup(bot:commands.Bot) ->None:
    await bot.add_cog(HelpCog(bot))