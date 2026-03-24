import re

def validate_webhook(url):
    """Checks if the URL matches standard Discord webhook formats."""
    pattern = r"^https://(discord|discordapp)\.com/api/webhooks/\d+/[a-zA-Z0-9_-]+$"
    return re.match(pattern, url)
