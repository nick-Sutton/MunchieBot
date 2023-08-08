import discord
from discord.ext import commands
from discord import app_commands
from messageformater import retrieve_current_games
from views import PaginationView

class Timer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="global", description="'@everyone' to notify the whole server")
    async def global_free_game(self, interaction: discord.Integration):
        globalEmbeds = retrieve_current_games()
        view = PaginationView(globalEmbeds)
        await interaction.response.send_message("@everyone",embed=view._initial, view=view, ephemeral=False)
    
async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(Timer(bot))