import os
import sys
import msvcrt
import subprocess
import threading
import asyncio
from colorama import init

# Custom Imports
from utils.common import purple, white, red, input_with_esc
from utils.functions.webhook import validate_webhook
from utils.ui import title, print_header, page_home, page_webhook, page_nuker, page_discord
from utils.functions.nuker import bot
from utils.functions.webhook import spammer, deleter, sender
from utils.functions.discord import account

# Global token state
discord_token = None
discord_username = None

def handle_discord(choice):
    global discord_token, discord_username
    
    if choice == '1':
        # Give Token
        token = input(f"\n{purple}[?]{white} Enter your Discord Token: ")
        if token.strip():
            discord_token = token.strip()
            # Get username
            discord_username = account.get_username(discord_token)
            print(f"\n{purple}[*]{white} Logged in as {discord_username}")
            import time
            time.sleep(1)
    elif choice == '5':
        # Change Token
        token = input(f"\n{purple}[?]{white} Enter new Discord Token: ")
        if token.strip():
            discord_token = token.strip()
            discord_username = account.get_username(discord_token)
            print(f"\n{purple}[*]{white} Token changed. Logged in as {discord_username}")
            import time
            time.sleep(1)
    elif discord_token:
        if choice == '1':
            # Delete Friends
            print(f"\n{purple}[*]{white} Deleting friends...")
            account.delete_friends(discord_token)
            account.update_profile(discord_token, discord_username)
            input(f"\n{purple}[?]{white} Press Enter to continue...")
        elif choice == '2':
            # Delete DMs
            print(f"\n{purple}[*]{white} Deleting DMs...")
            account.delete_dms(discord_token)
            account.update_profile(discord_token, discord_username)
            input(f"\n{purple}[?]{white} Press Enter to continue...")
        elif choice == '3':
            # Delete Servers
            print(f"\n{purple}[*]{white} Leaving/Deleting servers...")
            account.delete_servers(discord_token)
            account.update_profile(discord_token, discord_username)
            input(f"\n{purple}[?]{white} Press Enter to continue...")
        elif choice == '4':
            # Send Message
            msg = input(f"\n{purple}[?]{white} Enter message to send: ")
            if msg.strip():
                print(f"\n{purple}[*]{white} Sending message to all DMs and servers...")
                account.send_message(discord_token, msg.strip())
                account.update_profile(discord_token, discord_username)
            input(f"\n{purple}[?]{white} Press Enter to continue...")
    else:
        print(f"\n{purple}[!]{white} Please give a token first.")
        import time
        time.sleep(1)

def handle_webhook(choice):
    while True:
        webhook = input_with_esc(f"\n{purple}[?]{white} Enter Webhook URL (ESC to go back): ")
        
        # Handle ESC
        if webhook is None:
            return

        # Validation
        if validate_webhook(webhook):
            if choice == '1':
                spammer.run(webhook)
            elif choice == '2':
                deleter.run(webhook)
            elif choice == '3':
                sender.run(webhook)
            
            input(f"\n{purple}[?]{white} Press Enter to continue...")
            return
        else:
            print(f"{red}[!]{white} Webhook unrecognised, try again.")

def check_star():
    """Show star prompt and wait for user input"""
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        title()
        
        print(f"\n{purple}[{white} Star {purple}]{white} https://github.com/igNovoline/Nihil {purple}[{white} to gain access {purple}]{white}\n")
        
        choice = input(f"{purple}[{white} > {purple}]{white} Press Enter after starring the repo: ")
        
        # Simple check - just ask user to confirm
        print(f"\n{purple}[*]{white} Thank you! Proceeding...")
        import time
        time.sleep(1)
        break

def main():
    # Check if user starred the repo
    check_star()
    
    # Force standard output to use UTF-8 to support special characters like '─'
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    init(autoreset=True)
    pages = ["HOME", "DISCORD", "WEBHOOK", "NUKER"]
    current_page = 0
    bot_running = False
    global discord_token, discord_username

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        title()
        
        print_header(pages[current_page])

        if current_page == 0:
            page_home()
        elif current_page == 1:
            page_discord(discord_token is not None)
        elif current_page == 2:
            page_webhook()
        elif current_page == 3:
            page_nuker(bot_running)
        
        # Custom prompt based on page
        if current_page == 0 and discord_username:
            prompt = f"{purple}[ {white}{discord_username} {purple}]{white} > {white}"
        else:
            prompt = f"{purple}[ {white}> {purple}]{white}"
        
        print(f"\n{prompt}", end="", flush=True)
        
        key = msvcrt.getch()
        if key == b'\xe0': # Special keys (arrows)
            sub = msvcrt.getch()
            if sub == b'K': # Left Arrow
                current_page = (current_page - 1) % len(pages)
            elif sub == b'M': # Right Arrow
                current_page = (current_page + 1) % len(pages)
        elif key in [b'1', b'2', b'3', b'4', b'5', b'6']:
            choice = key.decode()
            print(choice) # Echo the number pressed

            if current_page == 0:
                # Home - no options, just navigation
                pass
            elif current_page == 1:
                # Discord page
                handle_discord(choice)
            elif current_page == 2 and choice in ['1', '2', '3']:
                handle_webhook(choice)
            elif current_page == 3:
                if bot_running:
                    if choice == '1':
                        # Stop Bot
                        bot.stop()
                        bot_running = False
                        print(f"\n{purple}[*]{white} Bot stopped.")
                        import time
                        time.sleep(1)
                    elif choice == '2':
                        # Change Token
                        token = input(f"\n{purple}[?]{white} Enter new Bot Token: ")
                        if token.strip():
                            bot.stop()
                            bot.start(token.strip())
                            print(f"\n{purple}[*]{white} Bot token changed.")
                        import time
                        time.sleep(1)
                    elif choice == '3':
                        # Exit
                        if bot_running:
                            bot.stop()
                        print(f"\n{purple}[*]{white} Exiting...")
                        sys.exit()
                    elif choice == '4':
                        # Show Commands Guide
                        print(f"\n{purple}[=== COMMANDS GUIDE ===]{white}")
                        print(f"{purple}!delete{white} - Delete all channels")
                        print(f"{purple}!ban{white}    - Ban all members")
                        print(f"{purple}!mute{white}   - Mute all members")
                        print(f"{purple}!nuke{white}   - Nuke the server")
                        print(f"\n{purple}[?]{white} Press Enter to continue...")
                        input()
                else:
                    if choice == '1':
                        # Start Bot - Ask for token first
                        token = input(f"\n{purple}[?]{white} Enter Bot Token: ")
                        if token.strip():
                            bot.start(token)
                            bot_running = True
                            print(f"\n{purple}[*]{white} Bot started.")
                            print(f"\n{purple}[=== COMMANDS ===]{white}")
                            print(f"{purple}!delete{white} - Delete all channels")
                            print(f"{purple}!ban{white}    - Ban all members")
                            print(f"{purple}!mute{white}   - Mute all members")
                            print(f"{purple}!nuke{white}   - Nuke the server")
                            print(f"\n{purple}[?]{white} Press Enter to continue...")
                            input()
                        else:
                            print(f"\n{purple}[!]{white} Token required to start bot.")
                        import time
                        time.sleep(1)
                    elif choice in ['2', '3', '4']:
                        print(f"\n{purple}[!]{white} Start the bot first.")
                        import time
                        time.sleep(1)

if __name__ == "__main__":
    main()
