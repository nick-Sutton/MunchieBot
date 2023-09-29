import discord
from discord.ext import commands
from typing import List
from collections import deque

class PaginationView(discord.ui.View):
    def __init__(self, embeds: List[discord.Embed]) -> None:
        super().__init__(timeout=None)
        self._embeds = embeds
        self._queue = deque(embeds)
        self._initial = embeds[0]
        self._len = len(embeds)
        self._current_page = 1
        self.children[0].disabled = True
        self._queue[0].set_footer(text=f"Pages {self._current_page}/{self._len}")

    @discord.ui.button(label="<", style=discord.ButtonStyle.blurple, custom_id="previous")
    async def previous(self, interaction:discord.Interaction, Button: discord.ui.button):
        self._queue.rotate(-1)
        embed = self._queue[0]
        self._current_page -= 1
        await self.update_buttons(interaction)
        await interaction.response.edit_message(embed=embed)

    @discord.ui.button(label=">", style=discord.ButtonStyle.blurple, custom_id="next")
    async def next(self, interaction:discord.Interaction, Button: discord.ui.button):
        self._queue.rotate(1)
        embed = self._queue[0]
        self._current_page += 1
        await self.update_buttons(interaction)
        await interaction.response.edit_message(embed=embed)

    async def update_buttons(self, interaction: discord.Interaction) -> None:
        for i in self._queue:
            i.set_footer(text=f"Pages {self._current_page}/{self._len}")
        if self._current_page == self._len:
            self.children[1].disabled = True
        else:
             self.children[1].disabled = False

        if self._current_page == 1:
            self.children[0].disabled = True
        else:
             self.children[0].disabled = False
                 
        await interaction.message.edit(view=self)       

        @property
        def initial(self) -> discord.Embed:
            return self._initial
        
class ViewBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents().all()
        intents.message_content = True
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=intents)
        self.cogs_List = ["cogs.freegamesCog", "cogs.globalCog", "cogs.helpCog", "epicSC"]

    async def setup_hook(self) -> None:
        for ext in self.cogs_List:
            await self.load_extension(ext)