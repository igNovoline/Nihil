import requests
import time
from utils.common import green, white, input_with_esc, red

def run(webhook_url):
    msg = input_with_esc(f"{green}[?]{white} Message to spam: ")
    if not msg: return

    print(f"{green}[+]{white} Spamming... (Press Ctrl+C to stop)")
    try:
        while True:
            requests.post(webhook_url, json={"content": msg})
            time.sleep(0.5)
    except KeyboardInterrupt:
        print(f"\n{red}[!]{white} Stopped.")