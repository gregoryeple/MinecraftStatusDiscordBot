import discord
from discord.ext import tasks
from mcstatus import JavaServer
from datetime import datetime, timedelta
import BotConfig

intents = discord.Intents.default()
client = discord.Client(intents = intents)

@tasks.loop(seconds = BotConfig.UPDATE_TIMER)
async def update_status():
    if client.is_closed():
        return
    server = JavaServer.lookup(BotConfig.SERVER_IP)
    timestamps = {}
    if BotConfig.SHOW_LAST_UPDATE_TIME:
        timestamps["start"] = int(datetime.now().timestamp() * 1000)
    if BotConfig.SHOW_UPDATE_TIMER:
        timestamps["end"] = int((datetime.now() + timedelta(seconds = BotConfig.UPDATE_TIMER)).timestamp() * 1000)
    try:
        status = server.status()
        activity = discord.Game(f"🟢 {status.players.online} / {status.players.max} players", timestamps = timestamps)
    except:
        activity = discord.Game("🔴 Offline", timestamps = timestamps)
    await client.change_presence(status = discord.Status.online, activity = activity)
    print(f"Updated status {activity.name}")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    await client.wait_until_ready()
    for guild in client.guilds:
        await change_nickname(guild)
    update_status.start()

@client.event
async def on_guild_join(guild):
    await change_nickname(guild)

async def change_nickname(guild):
    if not BotConfig.BOT_NAME:
        return
    bot_member = guild.get_member(client.user.id)
    if bot_member and bot_member.nick != BotConfig.BOT_NAME:
        try:
            await bot_member.edit(nick = BotConfig.BOT_NAME)
            print(f'Changed nickname to "{BotConfig.BOT_NAME}" in server: {guild.name}')
        except discord.Forbidden:
            print(f"Permission denied: Cannot change nickname in server: {guild.name}")
        except Exception as e:
            print(f"Failed to change nickname in server {guild.name}: {e}")

client.run(BotConfig.TOKEN)