import asyncio
from time import sleep
from datetime import datetime
import random
from typing import Literal, List

from constants import *

def update_status(msg: str, context: Literal["normal", "error", "warning", "info", "success"] = "normal"):
    """
    Print a message to the console with a timestamp and optional highlighting.

    The message can be highlighted by wrapping it in triple backticks (```).

    Args:
        msg (str): The message to print.
        context (str, optional): The context of the message. Default is "normal".
    """
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # Determine color based on context
    color = CONTEXT_COLORS.get(context, CONTEXT_COLORS["normal"])

    if "```" in msg:
        parts = msg.split("```")
        if len(parts) == 3:
            high_light_str = parts[1]
            highlighted_msg = f"{parts[0]}{CONTEXT_COLORS['hightlight']}{high_light_str}{color}{parts[2]}"
        else:
            highlighted_msg = msg
    else:
        highlighted_msg = msg
    
    print(color + str(current_time) + " - " + highlighted_msg)
    
def get_random_sec(a: int, b: int):
    if 0 < b < a:
        return random.randint(MIN_DELAY, MAX_DELAY)
    return random.randint(a if a > 0 else MIN_DELAY, b if b > 0 else MAX_DELAY)
    
def log_delay(sec):
    if sec < 60:
        # show mm:ss with mm=0
        formatted_time = f"00:{sec:02d}"
    elif sec < 3600:
        minutes = sec // 60
        seconds = sec % 60
        formatted_time = f"{minutes:02d}:{seconds:02d}"
    else:
        hours = sec // 3600
        remainder = sec % 3600
        minutes = remainder // 60
        seconds = remainder % 60
        formatted_time = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    update_status(f"delay for {formatted_time} seconds")
    
async def sleep_like_human(a: int = 0, b: int = 0, log=True):
    sec = get_random_sec(a, b)
    if log:
        log_delay(sec)

    await asyncio.sleep(sec)
    
    return True

def get_tagids_by_forum(formid: str) -> List[int]:
    return TAG_ID_BY_FORUM_CHANNEL.get(formid, None) # type: ignore

def get_promo():
    with open("promo.txt", "r") as f:
        title_content = f.read().split("\n---\n")
        return title_content[0], title_content[1]
