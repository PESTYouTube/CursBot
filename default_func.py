import asyncio
from os import getenv
from aiogram.filters import Command
from aiogram import Bot, Dispatcher, types, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

from text import STARTING_MESSAGE

router = Router()



@router.message(Command("start"))
async def startingMessage(message: types.Message) -> None:
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Запись на курсы",
        callback_data="curs_learn"
    ))
    builder.add(types.InlineKeyboardButton(
        text="Заказать практическую",
        callback_data="action_order"
    ))
    builder.adjust(2)
    await message.answer(STARTING_MESSAGE,
                         reply_markup=builder.as_markup())


@router.message(Command("help"))
async def help(message: types.Message) -> None:
    await message.answer("Помощь")
