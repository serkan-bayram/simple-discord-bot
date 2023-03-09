import discord
from discord.ext import tasks
import get_announs


intents = discord.Intents.default()
intents.message_content = True

# The client instance is our connection with Discord
client = discord.Client(intents=intents)


# Runs when the discord bot starts working
@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

    # Starting the loop
    default_loop.start()

# Run when certain message comes
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # Call the get_announs function by hand
    if message.content.startswith('/duyurular'):
        check, text = get_announs.announcements("call")
        
        await message.channel.send(text)

# Setting the loop
@tasks.loop(seconds = 300)
async def default_loop():
    channel = client.get_channel("your_channel_id")

    # Check is there any new announ
    check, content = get_announs.announcements("loop")

    if check:
        await channel.send(f"{content}")


with open("token.txt", "r") as f:
    TOKEN = f.read()

    client.run(TOKEN)



