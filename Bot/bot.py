from aiogram import Bot, Dispatcher
from Parser.parser import RssParser
from Bot.commands import baseRouter
from Config.json import getToken
import asyncio


class ParserBot:
    def __init__(self) -> None:
        self.token: str = getToken()
        self.bot: Bot = Bot(token=self.token)
        self.dp: Dispatcher = Dispatcher()
        self.dp.include_router(baseRouter)

        self.parser: RssParser = RssParser(bot=self.bot)
    
    async def startBot(self) -> None: 
        await self.bot.delete_webhook(drop_pending_updates=True)
        asyncio.create_task(self.parser.startAsync())
        await self.dp.start_polling(self.bot)
