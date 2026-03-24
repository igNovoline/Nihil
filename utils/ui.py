import os
from colorama import Style
from utils.common import purple, white

def title():
    print(f"""
        
        {purple}███{white}╗{purple}   ██{white}╗{purple}██{white}╗{purple}██{white}╗{purple}  ██{white}╗{purple}██{white}╗{purple}██{white}╗{purple}     
        ████{white}╗{purple}  ██{white}║{purple}██{white}║{purple}██{white}║{purple}  ██{white}║{purple}██{white}║{purple}██{white}║{purple}     
        ██{white}╔{purple}██{white}╗{purple} ██{white}║{purple}██{white}║{purple}███████{white}║{purple}██{white}║{purple}██{white}║{purple}
        ██{white}║╚{purple}██{white}╗{purple}██{white}║{purple}██{white}║{purple}██{white}╔══{purple}██{white}║{purple}██{white}║{purple}██{white}║{purple}     
        ██{white}║ ╚{purple}████{white}║{purple}██{white}║{purple}██{white}║  {purple}██{white}║{purple}██{white}║{purple}███████{white}╗{purple}
        {white}╚═╝  ╚═══╝╚═╝╚═╝  ╚═╝╚═╝╚══════╝
               [ by novoline ]
""")

def page_home():
    print(f"{white}Welcome to {purple}Nihil{white}!, a Discord toolkit for all your needs")
    print(f"consider starring my github repo: {purple}{"https://github.com/igNovoline/Nihil"}{white} to support me, thanks!")
    print(f"""
Use the {purple}arrow keys{white} to navigate between pages.""")


def print_header(page_name):
    try:
        width = os.get_terminal_size().columns
    except OSError:
        width = 80
    prefix_len = len(page_name) + 6
    dashes = "─" * (max(0, width - prefix_len))
    print(f"{purple}[ {white}{page_name}{purple} ] {dashes}\n")

def page_webhook():
    print(f"    {purple}[1]{white} Spam Webhook        {purple}║ {purple}[3]{white} Send Message")
    print(f"    {purple}[2]{white} Delete Webhook")

def page_nuker(bot_running=False):
    if bot_running:
        print(f"    {purple}[1]{white} Stop Bot")
        print(f"    {purple}[2]{white} Change Token      {purple}║ {purple}[4]{white} Show Commands")
        print(f"    {purple}[3]{white} Exit")
    else:
        print(f"    {purple}[1]{white} Start Bot")

def page_discord(logged_in=False):
    if not logged_in:
        print(f"    {purple}[1]{white} Give Token")
    else:
        print(f"    {purple}[1]{white} Delete Friends      {purple}║ {purple}[4]{white} Send Message")
        print(f"    {purple}[2]{white} Delete DMs          {purple} {purple}[5]{white} Change Token")
        print(f"    {purple}[3]{white} Delete Servers")
