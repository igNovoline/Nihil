import requests
from utils.common import green, white, input_with_esc

def run(webhook_url):
    msg = input_with_esc(f"{green}[?]{white} Message to send: ")
    if not msg: return

    requests.post(webhook_url, json={"content": msg})
    print(f"{green}[+]{white} Sent.")