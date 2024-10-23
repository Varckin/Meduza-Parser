from aiogram import Bot, Dispatcher
from Bot.commands import baseRouter, bot
from Config.json import getToken


class ParserBot:
    def __init__(self) -> None:
        global bot
        self.token: str = getToken()
        self.bot: Bot = Bot(token=self.token)
        bot = self.bot
        self.dp: Dispatcher = Dispatcher()
        self.dp.include_router(baseRouter)
    
    async def startBot(self) -> None: 
        await self.bot.delete_webhook(drop_pending_updates=True)
        await self.dp.start_polling(self.bot)
