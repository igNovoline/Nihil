import msvcrt
import sys
import re
from colorama import Fore, Style

# Colors
purple = Fore.LIGHTMAGENTA_EX
white = Fore.LIGHTWHITE_EX
red = Fore.LIGHTRED_EX
green = Fore.LIGHTGREEN_EX

def validate_webhook(url):
    """Checks if the URL matches standard Discord webhook formats."""
    pattern = r"^https://(discord|discordapp)\.com/api/webhooks/\d+/[a-zA-Z0-9_-]+$"
    return re.match(pattern, url)

def input_with_esc(prompt):
    """
    Custom input that allows the user to press ESC to cancel.
    Returns the string entered, or None if ESC was pressed.
    """
    sys.stdout.write(prompt)
    sys.stdout.flush()
    buffer = []
    while True:
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'\x1b': # ESC key
                print()
                return None
            elif key == b'\r': # Enter key
                print()
                return "".join(buffer)
            elif key == b'\x08': # Backspace
                if buffer:
                    buffer.pop()
                    sys.stdout.write('\b \b')
                    sys.stdout.flush()
            else:
                try:
                    char = key.decode()
                    buffer.append(char)
                    sys.stdout.write(char)
                    sys.stdout.flush()
                except:
                    pass