import asyncio
from Bot.bot import ParserBot


if __name__ == "__main__":
    try:
        bot: ParserBot = ParserBot()
        asyncio.run(bot.startBot())
    except Exception as e:
        print(e)
