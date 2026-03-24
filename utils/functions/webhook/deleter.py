import requests
from utils.common import green, white, red

def run(webhook_url):
    print(f"{green}[*]{white} Deleting webhook...")
    response = requests.delete(webhook_url)
    if response.status_code in [204, 200]:
        print(f"{green}[+]{white} Webhook deleted successfully.")
    else:
        print(f"{red}[!]{white} Failed to delete webhook.")