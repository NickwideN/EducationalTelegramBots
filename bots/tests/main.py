from datetime import datetime

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, \
    CallbackQuery
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from config_reader import env

# Создаем объекты бота и диспетчера
bot = Bot(token=env('BOT_TOKEN'))
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    button_1: InlineKeyboardButton = InlineKeyboardButton(
        text="Кнопка 1",
        callback_data="button_1"
    )

    button_2: InlineKeyboardButton = InlineKeyboardButton(
        text="Кнопка 2",
        callback_data="button_2"
    )

    # Создаем список списков с кнопками
    keyboard: list[list[InlineKeyboardButton]] = [
        [button_1],
        [button_2]
    ]

    # Создаем объект клавиатуры, добавляя в него кнопки
    my_keyboard = InlineKeyboardMarkup(
        inline_keyboard=keyboard,
    )

    await message.answer('Привет!\nБот для тестов на связи!\n'
                         'С моей помощью мой хозяин упражняется в реализации разных фич', reply_markup=my_keyboard)


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Бот для тестов'
    )


# хендлер, который обрабатывает callback button_1
@dp.callback_query(F.data == "button_1")
async def process_callback_button_1(callback: CallbackQuery):
    # await callback.message.answer(text='Кнопка 1')
    if callback.message.text != 'Вы нажали на кнопку 1':
        await callback.message.edit_text(
            'Вы нажали на кнопку 1',
            reply_markup=callback.message.reply_markup
        )
    await callback.answer()


# хендлер, который обрабатывает callback button_2
@dp.callback_query(F.data == "button_2")
async def process_callback_button_2(callback: CallbackQuery):
    await callback.message.answer(text='Кнопка 2')
    if callback.message.text != 'Вы нажали на кнопку 2':
        await callback.message.edit_text(
            'Вы нажали на кнопку 2',
            reply_markup=callback.message.reply_markup
        )
    await callback.answer()


@dp.message()
async def process_other_masseges(message: Message):
    await message.answer(text='Это бот для тестов, привет)')

if __name__ == '__main__':
    dp.run_polling(bot)
