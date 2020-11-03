import boto3
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix="!")

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('bot')


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")


@bot.command(name="watch", brief="add symbol to table")
async def add_watch_entry(ctx, symbol):
    response = table.put_item(
        Item={"symbol": symbol}
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        await ctx.send(f"I am watching {symbol}!")
    else:
        await ctx.send(response)


@bot.command(name="unwatch", brief="remove symbol from table")
async def remove_watch_entry(ctx, symbol):
    response = table.delete_item(
        Item={"symbol": symbol}
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        await ctx.send(f"I am not watching {symbol} anymore.")
    else:
        await ctx.send(response)


@bot.command(name="watching", brief="show all symbols under watch")
async def show_all_watch_entries(ctx):
    response = table.scan(Limit=1000)

    embed = discord.Embed(title="watching table").add_field(name="id", value="symbol")
    for i, item in enumerate(response["Items"]):
        embed.add_field(name=str(i), value=item["symbol"])

    await ctx.send(embed=embed)


if __name__ == '__main__':
    bot.run("MY_TOKEN")
