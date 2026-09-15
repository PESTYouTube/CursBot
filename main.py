import asyncio
from os import getenv
from aiogram.filters import Command
from aiogram import Bot, Dispatcher, types
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State

TOKEN = "8660961782:AAFSAGSzJIARBalfZtDYW3FNLbCEtCNcgJU"
CHAT_ADMIN = -1004356211402
ORDER_CHAT_ADMIN = 2
dp = Dispatcher()
processed_albums = set()

@dp.message(Command("start"))
async def start(message: types.Message) -> None:
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
    await message.answer("Привет ты решил подтянуть свои знания в языках программирования"+
                         " или лень писать практические работы ты попал туда куда надо!\n"+
                         "Выбери что тебе нужно сделать опиши и мы с тобой свяжемся в ближайшее время!",
                         reply_markup=builder.as_markup())
    # await message.bot.send_message(chat_id = CHAT_ADMIN,text=f"Пользователь {message.from_user.username} запустил бота")



@dp.message(Command("help"))
async def help(message: types.Message) -> None:
    await message.answer("Помощь")

class OrderStates(StatesGroup):
    waiting_for_description = State()  # Состояние: бот ждет описание от пользователя


@dp.callback_query()
async def action_order(callback: types.CallbackQuery, state: FSMContext):
    if callback.data == "curs_learn":
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="Python",
            callback_data="learn_python",
        ))
        builder.add(types.InlineKeyboardButton(
            text="PostgreSQL",
            callback_data="learn_SQL",
        ))
        builder.add(types.InlineKeyboardButton(
            text="Назад",
            callback_data="back_to_start",
        ))
        builder.adjust(2)
        await callback.message.edit_text("Отлично! Теперь выбери какой язык программирования ты хочешь?",
                                      reply_markup=builder.as_markup()
        )
    elif callback.data == "back_to_start":
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
        await callback.message.edit_text("Привет ты решил подтянуть свои знания в языках программирования" +
                             " или лень писать практические работы ты попал туда куда надо!\n" +
                             "Выбери что тебе нужно сделать опиши и мы с тобой свяжемся в ближайшее время!",
                             reply_markup=builder.as_markup())
        await callback.answer()

    elif callback.data == "learn_SQL":
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="Записаться",
            callback_data="curse_order_sql"
        ))
        builder.add(types.InlineKeyboardButton(
            text="Назад",
            callback_data="back_to_start"
        ))
        await callback.message.edit_text("Идет загрузка данных")
        await callback.message.edit_text("Прайс лист:\nОдин урок - 1000\n4 урока - 3500\n8 уроков - 6000",
                                         reply_markup=builder.as_markup())
    elif callback.data == "learn_python":
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="Записаться",
            callback_data="curse_order_python"
        ))
        builder.add(types.InlineKeyboardButton(
            text="Назад",
            callback_data="back_to_start"
        ))
        await callback.message.edit_text("Идет загрузка данных")
        await callback.message.edit_text("Прайс лист:\nОдин урок - 1000\n4 урока - 3500\n8 уроков - 6000",reply_markup=builder.as_markup())


        await callback.answer()

    elif callback.data == "action_order":
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="Назад",
            callback_data="back_to_start"
        ))
        await callback.message.edit_text("Опиши что тебе необходимо написать, отправь фото или вставь текст",reply_markup=builder.as_markup())
        await state.set_state(OrderStates.waiting_for_description)
        await callback.answer()

    elif callback.data == "curse_order_sql":
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="Заказать снова",
            callback_data="back_to_start"
        ))
        await callback.message.edit_text("Ты успешно записался на курс в скором времени тебе напишет администратор",
                                         reply_markup=builder.as_markup())
        admin_text = (
            f"**Новый заказ!**\n"
            f"От кого @{callback.from_user.username} (id: {callback.from_user.id})\n"
            f"Описание: \n"
            f"Запись на курс по SQL!"
        )
        await callback.bot.send_message(
            chat_id=CHAT_ADMIN,
            message_thread_id=ORDER_CHAT_ADMIN,
            text=admin_text,
            parse_mode="Markdown"
        )

        await callback.answer()

    elif callback.data == "curse_order_python":
        builder = InlineKeyboardBuilder()
        builder.add(types.InlineKeyboardButton(
            text="Заказать снова",
            callback_data="back_to_start"
        ))
        await callback.message.edit_text("Ты успешно записался на курс в скором времени тебе напишет администратор",reply_markup=builder.as_markup())
        admin_text = (
        f"**Новый заказ!**\n"
        f"От кого @{callback.from_user.username} (id: {callback.from_user.id})\n"
        f"Описание: \n"
        f"Запись на курс по Python!"
    )
        await callback.bot.send_message(
            chat_id=CHAT_ADMIN,
            message_thread_id=ORDER_CHAT_ADMIN,
            text=admin_text,
            parse_mode="Markdown"
        )

        await callback.answer()


@dp.message(OrderStates.waiting_for_description)
async def process_order_description(message: types.Message, state: FSMContext):
    await message.edit_text("Спасибо! Ваша заявка принята. Мы свяжемся с вами в ближайшее время")
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Заказать снова",
        callback="back_to_start"
    ))
    await message.answer()

    username = f"@{message.from_user.username}" if message.from_user.username else message.from_user.first_name
    user_id = message.from_user.id

    user_text = message.text if message.text else (message.caption if message.caption else "Без текста")
    admin_text = (
        f"**Новый заказ!**\n"
        f"От кого @{username} (id: {user_id})\n"
        f"Описание: \n"
        f"{user_text}"
    )

    if message.media_group_id:
        mg_id = message.media_group_id

        # Чтобы плашка админу пришла строго ОДИН раз для всего альбома
        if mg_id not in processed_albums:
            processed_albums.add(mg_id)

            # Отправляем админу ваш текст в качестве анонса к альбому
            await message.bot.send_message(
                chat_id=CHAT_ADMIN,
                text=f"{admin_text}\n\n👇 Все фото альбома прикреплены ниже:",
                parse_mode="Markdown"
            )
            async def clear_album(album_id):
                await asyncio.sleep(2)
                processed_albums.discard(album_id)
                await state.clear()

            asyncio.create_task(clear_album(mg_id))
            await state.clear()

        # Пересылаем ВСЕ фотографии альбома по очереди (они склеятся в один пост)
        await message.send_copy(chat_id=CHAT_ADMIN,message_thread_id=ORDER_CHAT_ADMIN)

    elif message.photo:
        photo_id = message.photo[-1].file_id
        await message.bot.send_photo(
            chat_id=CHAT_ADMIN,
            message_thread_id=ORDER_CHAT_ADMIN,
            photo=photo_id,
            caption=admin_text,
            parse_mode="Markdown"
        )
        await state.clear()
    else:
        await message.bot.send_message(
            chat_id=CHAT_ADMIN,
            message_thread_id=ORDER_CHAT_ADMIN,
            text=admin_text,
            parse_mode="Markdown"
        )
        await state.clear()

















async def main() -> None:
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())



















