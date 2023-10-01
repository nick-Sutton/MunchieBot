import time, platform, sys
from art import *
from rich.console import Console
from rich.text import Text
from rich.theme import Theme

THEME = Theme({"success": "white on green","error":"white on red","headerTitles": "red", "headerdescs": "bright_green"})
CONSOLE = Console(theme = THEME)

def console_layout():
    art = text2art("OATS_",font = "larry3d")
    logo = Text(art)
    logo.stylize("deep_pink2")
    CONSOLE.print(logo)

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    CONSOLE.print("Time:            ", style="headerTitles", end =" ")
    CONSOLE.print(current_time, style="headerdescs")

    CONSOLE.print("Created By:      ", style="headerTitles", end =" ")
    CONSOLE.print("https://github.com/nick-Sutton", style="headerdescs")

    CONSOLE.print("© 2023 Sutton:  ", style="headerTitles", end =" ")
    CONSOLE.print(" MIT License", style="headerdescs")

    CONSOLE.print("OS:              ", style="headerTitles", end =" ")
    CONSOLE.print(platform.system(), style="headerdescs")

    CONSOLE.print("Language:        ", style="headerTitles", end =" ")
    CONSOLE.print(sys.prefix, style="headerdescs")
