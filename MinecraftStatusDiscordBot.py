import discord
from mcstatus import JavaServer
import asyncio
import BotConfig

intents = discord.Intents.default()
client = discord.Client(intents = intents)

async def update_status():
    await client.wait_until_ready()
    while not client.is_closed():
        server = JavaServer.lookup(BotConfig.SERVER_IP)
        try:
            status = server.status()
            activity = discord.Game(f":green_circle: {status.players.online} / {status.players.max} players")
        except:
            activity = discord.Game("red_circle: Offline")
        await client.change_presence(status = discord.Status.online, activity = activity)
        await asyncio.sleep(BotConfig.UPDATE_TIME)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

client.loop.create_task(update_status())
client.run(BotConfig.TOKEN)