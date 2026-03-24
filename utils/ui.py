import os
from colorama import Style
from utils.common import purple, white

def title():
    print(purple + Style.BRIGHT)
    print("""
                                        _____   ____________ ___________
                                        ___  | / /__(_)__  /____(_)__  /
                                        __   |/ /__  /__  __ \_  /__  / 
                                        _  /|  / _  / _  / / /  / _  /  
                                        /_/ |_/  /_/  /_/ /_//_/  /_/      [By Novoline]
""")

def print_header(page_name):
    try:
        width = os.get_terminal_size().columns
    except OSError:
        width = 80
    prefix_len = len(page_name) + 6
    dashes = "─" * (max(0, width - prefix_len))
    print(f"{purple}[ {white}{page_name}{purple} ] {dashes}\n")

def page_discord():
    print(f"    {purple}[1]{white} Spam Webhook        {purple}| {purple}[3]{white} Send Message")
    print(f"    {purple}[2]{white} Delete Webhook")

def page_nuker(bot_running=False):
    if bot_running:
        print(f"    {purple}[1]{white} Stop Bot")
        print(f"    {purple}[2]{white} Show Commands Guide")
        print(f"\n{purple}[ Bot Running ]{white} Prefix: {purple}!{white}")
    else:
        print(f"    {purple}[1]{white} Start Bot")