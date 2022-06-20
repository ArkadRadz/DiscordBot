from wordle import wordle
from karma import karma
from config import get_bot_token

from discord.ext import commands
import discord

intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

bot.add_cog(wordle(bot))
bot.add_cog(karma(bot))
bot.run(get_bot_token())