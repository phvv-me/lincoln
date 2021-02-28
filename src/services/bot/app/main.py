import discord
from discord.ext import commands

from common.tables import Table

bot = commands.Bot(command_prefix="!")

table = Table('watchlist')

# TODO: add logger


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    # ctx.send(f"{bot.user} has connected to Discord!")


@bot.command(name="watch", brief="add symbol to table")
async def add_watch_entry(ctx, symbol):
    response = table.put(symbol=symbol)

    if response.is_successful:
        await ctx.send(f"I am watching {symbol}!")
    else:
        await ctx.send("[ERROR] Unable to add symbol to watchlist")


@bot.command(name="unwatch", brief="remove symbol from table")
async def remove_watch_entry(ctx, symbol):
    response = table.delete(symbol=symbol)

    if response.is_successful:
        await ctx.send(f"I am not watching {symbol} anymore.")
    else:
        await ctx.send("[ERROR] Unable to remove symbol from watchlist")


@bot.command(name="watching", brief="show all symbols under watch")
async def show_all_watch_entries(ctx):
    response = table.scan()

    if response.is_successful:
        embed = discord.Embed(title="watching table").add_field(name="id", value="symbol")
        for i, item in enumerate(response.data):
            embed.add_field(name=str(i), value=item["symbol"])
        await ctx.send(embed=embed)
    else:
        await ctx.send("No items found in watchlist table")


