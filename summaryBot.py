import os
import openai
import discord
from discord.ext import commands
from collections import deque

intents = discord.Intents.default()
intents.typing = False
intents.presences = False
