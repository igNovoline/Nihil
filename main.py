import os
import sys
import msvcrt
import subprocess
import threading
import asyncio
from colorama import init

# Custom Imports
from utils.common import purple, white, red, input_with_esc, validate_webhook
from utils.ui import title, print_header, page_discord, page_nuker
from utils.functions.nuker import bot
from utils.functions.discord import spammer, deleter, sender

def handle_discord(choice):
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

def main():
    # Force standard output to use UTF-8 to support special characters like '─'
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    init(autoreset=True)
    pages = ["DISCORD", "NUKER"]
    current_page = 0
    bot_running = False

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        title()
        
        print_header(pages[current_page])

        if current_page == 0:
            page_discord()
        elif current_page == 1:
            page_nuker(bot_running)
        
        print(f"\n{purple}[ > ] {white}", end="", flush=True)
        
        key = msvcrt.getch()
        if key == b'\xe0': # Special keys (arrows)
            sub = msvcrt.getch()
            if sub == b'K': # Left Arrow
                current_page = (current_page - 1) % len(pages)
            elif sub == b'M': # Right Arrow
                current_page = (current_page + 1) % len(pages)
        elif key in [b'1', b'2', b'3', b'4']:
            choice = key.decode()
            print(choice) # Echo the number pressed

            if current_page == 0 and choice in ['1', '2', '3']:
                handle_discord(choice)
            elif current_page == 1:
                if bot_running:
                    if choice == '1':
                        # Stop Bot
                        bot.stop()
                        bot_running = False
                        print(f"\n{purple}[*]{white} Bot stopped.")
                        import time
                        time.sleep(1)
                    elif choice == '2':
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