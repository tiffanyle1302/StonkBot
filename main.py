"""Needed imports for functions"""
import os
import logging
import discord
from polygon import RESTClient
from dotenv import load_dotenv
from discord.ext import commands


# TODO: Get polygon set up correctly

"""Discord Bot Set-Up with Intents"""
load_dotenv() #load API key
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

"""Have to set intents for bot to work because discord is qUiRkY"""
bot = commands.Bot(command_prefix='?', intents=intents)

"""Polygon set up"""
POLYGON_TOKEN = str(os.environ.get("POLYGON_TOKEN"))
client = RESTClient(api_key = POLYGON_TOKEN)


def retrieving_aggs(stock: str, day: str):
    """Get Aggregate Data in the form of a string"""
    aggs = client.get_aggs(
        ticker = stock,
        multiplier = 1,
        timespan = "day",
        from_ = day,
        to = day,
    )
    return aggs[0]
    

def test_run():
    aggs = client.get_aggs(
       "AAPL",
        1,
        "day",
        "2022-04-04",
        "2022-04-04",
    )
    return str(aggs[0])


"""All bot Commands below"""
@bot.event
async def on_ready():
    """Prints message that it's online"""
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')


@bot.command()
async def test(ctx, arg):
    """test command to check bot replies back"""
    await ctx.send(arg)


@bot.command()
async def add(ctx, a: int, b: int):
    """test bot ability to reply with correct computations"""
    await ctx.send(a + b)

@bot.command()
async def daggs(ctx, stock: str, day: str): #day has to be formatted as YYYY-MM-DD
    """Get aggregates data of stocks within the day of request"""
    output = retrieving_aggs(stock, day)
    await ctx.send(output)
    


"""Connect to discord servers needed to run"""
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

DISCORD_TOKEN = str(os.environ.get("DISCORD_TOKEN"))
bot.run(DISCORD_TOKEN, log_handler=handler, log_level=logging.DEBUG)
