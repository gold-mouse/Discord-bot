import os
from dotenv import load_dotenv

from colorama import Fore, Style, init

load_dotenv()

init(autoreset=True) # ensures that styles reset automatically after each print, which helps avoid color bleeding.

DISCORD_AUTH_TOKEN = os.getenv("DISCORD_AUTH_TOKEN", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MIN_DELAY = int(os.getenv("MIN_DELAY", 30)) * 60 # in seconds
MAX_DELAY = int(os.getenv("MAX_DELAY", 60)) * 60 # in seconds
CHAT_ID = os.getenv("CHAT_ID", "")
BOT_TOKEN = os.getenv("BOT_TOKEN", "")

CONTEXT_COLORS = {
    "error": Fore.RED,
    "warning": Fore.YELLOW,
    "info": Fore.BLUE,
    "success": Fore.GREEN,
    "normal": Fore.WHITE,
    "hightlight": Fore.CYAN
}

RESET_STYLE = Style.RESET_ALL
