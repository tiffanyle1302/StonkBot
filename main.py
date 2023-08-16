"""Needed imports for functions"""
import os
import logging
import logging.handlers
import discord
from polygon import RESTClient
from dotenv import load_dotenv
from discord.ext import commands



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

def extract_parameters(input_string):
    """Removes Prefix(), and only returns the needed info"""
    start_index = input_string.find("(") + 1
    end_index = input_string.rfind(")")
    parameters = input_string[start_index:end_index]
    return parameters

def get_crypto_aggs(crypto: str, day: str):
    """Get Aggregate Data in the form of a string"""
    aggs = client.get_daily_open_close_agg(
        ticker = crypto,
        date = day,
    )
    whole_data = str(aggs)
    clean = extract_parameters(whole_data)
    return clean

def get_stock_aggs(stock: str, day: str):
    """Get Aggregate Data in the form of a string"""
    aggs = client.get_daily_open_close_agg(
        ticker = stock,
        date = day,
    )
    whole_data = str(aggs)
    clean = extract_parameters(whole_data)
    return clean
    
def test_run():
    """test function of retrieving aggs"""
    aggs = client.get_aggs(
       "AAPL",
        1,
        "day",
        "2022-04-04",
        "2022-04-04",
    )
    return str(aggs[0])

"""Help Command Set Up"""
class HelpSetUp(commands.MinimalHelpCommand):
    """Sets up the help page"""
    async def send_pages(self):
        destination = self.get_destination()
        emby = discord.Embed(title = "Help", 
                             description = "Use ?help [name] to get a detail info on the specific command", 
                             colour = discord.Color.random())
        emby.add_field(name = "Business Commands", value = "daggs, cryaggs")
        emby.add_field(name = "Fun and Test Commands", value = "test, add")
        await destination.send(embed = emby)
    
    async def send_command_help(self, command):
        emby = discord.Embed(title = self.get_command_signature(command), colour = discord.Color.random())
        if command.help:
            emby.description = command.help
        if alias := command.aliases:
            emby.add_field(name="Aliases", value=", ".join(alias), inline=False)
        channel = self.get_destination()
        await channel.send(embed = emby)

bot.help_command = HelpSetUp()



"""All bot Commands below"""
@bot.event
async def on_ready():
    """Prints message that it's online"""
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

@bot.command()
async def test(ctx, statement):
    """Test command to check bot replies back."""
    await ctx.send(statement)


@bot.command()
async def add(ctx, a: int, b: int):
    """Adds two numbers and returns its sum."""
    await ctx.send(a + b)



"""Business related commands"""
@bot.command()
async def daggs(ctx, stock: str, date: str): #day has to be formatted as YYYY-MM-DD
    """Get aggregates data of stocks for the requested day. **Note: date needs to be formatted as YYYY-MM-DD**"""
    output = get_stock_aggs(stock, date)
    await ctx.send(output)

@bot.command()
async def cryaggs(ctx, crypto: str, day: str):
    """Get aggregate data of crypto for the requested day. **Note: date needs to be formatted as YYYY-MM-DD**"""
    output = get_crypto_aggs(crypto, day)
    await ctx.send(output)

#TODO: make specific aggs
@bot.command
async def 

"""Error Handling for commands"""
@test.error
async def test_error(ctx, error):
    """Throws error for ?test"""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("I'm missing a statement parameter. Use ?help for clarification")

@add.error
async def add_error(ctx, error):
    """Throws error for ?add"""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("I'm missing one or two integer parameters. Use ?help for clarification.")

@daggs.error
async def daggs_error(ctx, error):
    """Throws error for ?daggs"""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("I'm missing parameters. Use ?help for clarification.")
    elif isinstance(error, commands.BadArgument):
        await ctx.reply("Unable to get data on date or date is in a incorrect format. Use ?help for clarification.")

@cryaggs.error
async def cryaggs_error(ctx, error):
    """Throws error for ?cryaggs"""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.reply("I'm missing parameters. Use ?help for clarification.")
    elif isinstance(error, commands.BadArgument):
        await ctx.reply("Unable to get data on date or date is in a incorrect format. Use ?help for clarification.")



"""Logging Data for checking errors"""
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

"""Connect to discord servers needed to run"""
DISCORD_TOKEN = str(os.environ.get("DISCORD_TOKEN"))
bot.run(DISCORD_TOKEN)
