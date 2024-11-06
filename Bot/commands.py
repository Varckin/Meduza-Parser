from aiogram import Router
from aiogram import F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from Config.json import actionsub, writeIdUser


baseRouter: Router = Router()


def keyboard() -> ReplyKeyboardMarkup:
    addSub: KeyboardButton = KeyboardButton(text="Подписаться 👍🏻")
    delSub: KeyboardButton = KeyboardButton(text="Отписаться 👎🏻")

    return ReplyKeyboardMarkup(keyboard=[[delSub, addSub]], resize_keyboard=True)

@baseRouter.message(Command("start"))
async def cmd_start(message: Message):
    actionsub(idUser=message.chat.id, action="add")
    writeIdUser(idUser=message.chat.id, fullName=message.chat.full_name)
    await message.answer(text="Привет вы подписались на новости от Медузы.")

@baseRouter.message(Command("subscription"))
async def cmd_start(message: Message):
    await message.answer(text="Выберите что сделать с подписотой.", reply_markup=keyboard())

@baseRouter.message(F.text == "Подписаться 👍🏻")
async def cmd_start(message: Message):
    await message.answer(text=actionsub(idUser=message.chat.id, action="add"), reply_markup=ReplyKeyboardRemove())

@baseRouter.message(F.text == "Отписаться 👎🏻")
async def cmd_start(message: Message):
    await message.answer(text=actionsub(idUser=message.chat.id, action="del"), reply_markup=ReplyKeyboardRemove())
