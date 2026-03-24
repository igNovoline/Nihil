
import discord
import asyncio

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"USERNAME|{client.user.name}")
    await client.close()

asyncio.run(client.start("asdw"))
