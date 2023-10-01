from dotenv import load_dotenv
from consoleheader import console_layout
import os

load_dotenv()
console_layout()
TOKEN = os.getenv("TOKEN") #Add your own token here
CHANNEL_ID = os.getenv("CHANNEL_ID")  #Add your own channel ID here
