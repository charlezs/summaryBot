import os
import openai
import discord
from discord.ext import commands
from collections import deque
from dotenv import load_dotenv
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()


import ssl
ssl.match_hostname = lambda cert, hostname: True


intents = discord.Intents.default()
intents.typing = False
intents.presences = False

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

bot = commands.Bot(command_prefix="!", intents=intents, trust_env=True)
openai.api_key = OPENAI_API_KEY

MAX_MESSAGES = 10
message_queue = deque(maxlen=MAX_MESSAGES)

@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    message_queue.append(message)

    if len(message_queue) == MAX_MESSAGES:
        await summarize_messages()

    await bot.process_commands(message)

async def summarize_messages():
    text = "\n\n".join([msg.content for msg in message_queue])

    prompt = f"Please summarize the following conversation into bullet points:\n\n{text}\n\nSummary:"
    response = openai.Completion.create(engine="text-davinci-002", prompt=prompt, max_tokens=150, n=1, stop=None, temperature=0.5)

    summary = response.choices[0].text.strip()
    summary_bullet_points = summary.split("\n")

    channel = bot.get_channel(985520885538643968)
    await channel.send("Conversation summary:")
    for point in summary_bullet_points:
        await channel.send(f"- {point}")

bot.run(DISCORD_TOKEN)
