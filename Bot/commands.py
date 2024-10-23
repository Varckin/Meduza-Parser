from aiogram import Router
from aiogram import Bot
from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from Parser.parser import RssParser
from Config.json import actionsub


baseRouter: Router = Router()
bot: Bot = None

def keyboard() -> ReplyKeyboardMarkup:
    addSub: KeyboardButton = KeyboardButton(text="Подписаться 👍🏻")
    delSub: KeyboardButton = KeyboardButton(text="Отписаться 👎🏻")

    return ReplyKeyboardMarkup(keyboard=[[delSub, addSub]], resize_keyboard=True)

@baseRouter.message(Command("start"))
async def cmd_start(message: Message):
    parser: RssParser = RssParser(bot=bot)
    actionsub(idUser=message.chat.id, action="add")
    await message.answer(text="Привет вы подписались на новости от Медузы.")


@baseRouter.message(Command("subscription"))
async def cmd_start(message: Message):
    await message.answer(text="Выберите что сделать с подписотой.", reply_markup=keyboard())

@baseRouter.message(F.text == "Подписаться 👍🏻")
async def cmd_start(message: Message):
    print("1")
    await message.answer(text=actionsub(idUser=message.chat.id, action="add"), reply_markup=ReplyKeyboardRemove())

@baseRouter.message(F.text == "Отписаться 👎🏻")
async def cmd_start(message: Message):
    print("0")
    await message.answer(text=actionsub(idUser=message.chat.id, action="del"), reply_markup=ReplyKeyboardRemove())
