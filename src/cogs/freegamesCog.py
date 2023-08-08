import discord
from discord.ext import commands
from discord import app_commands
from messageformater import retrieve_current_games
from views import PaginationView

class FreeGamesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="freegame", description="See the latest free game on Epic")
    async def FreeGameCog(self, interaction: discord.Interaction):
        embeds = retrieve_current_games()
        view = PaginationView(embeds)
        await interaction.response.send_message(embed=view._initial, view=view, ephemeral=False)

async def setup(bot:commands.Bot) -> None:
    await bot.add_cog(FreeGamesCog(bot))
