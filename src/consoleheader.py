import time, platform, sys
from art import *
from rich.console import Console
from rich.text import Text
from rich.theme import Theme

def info_layout():
    custom_theme = Theme({"success": "white on green","error":"white on red","headerTitles": "red", "headerdescs": "bright_green"})
    console = Console(theme = custom_theme)

    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)

    console.print("Time:            ", style="headerTitles", end =" ")
    console.print(current_time, style="headerdescs")

    console.print("Created By:      ", style="headerTitles", end =" ")
    console.print("https://github.com/nick-Sutton", style="headerdescs")

    console.print("© 2023 Sutton:  ", style="headerTitles", end =" ")
    console.print(" MIT License", style="headerdescs")

    console.print("OS:              ", style="headerTitles", end =" ")
    console.print(platform.system(), style="headerdescs")

    console.print("Language:        ", style="headerTitles", end =" ")
    console.print(sys.prefix, style="headerdescs")

def logo_format():
    custom_theme = Theme({"success": "white on green","error":"white on red","headerTitles": "red", "headerdescs": "dark_slate_gray2"})
    console = Console(theme = custom_theme)

    art = text2art("OATS_",font = "larry3d")
    logo = Text(art)
    logo.stylize("deep_pink2")
    console.print(logo)
