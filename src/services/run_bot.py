from decouple import config

from bot.app.main import bot

if __name__ == '__main__':
    TOKEN = config("DISCORD_TOKEN")
    bot.run(TOKEN)