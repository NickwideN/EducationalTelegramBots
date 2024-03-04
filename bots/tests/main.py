from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from config_reader import env

# Создаем объекты бота и диспетчера
bot = Bot(token=env('BOT_TOKEN'))
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):

    url_button_1: InlineKeyboardButton = InlineKeyboardButton(
        text="Мой телеграм канал",
        url="tg://resolve?domain=nickwiden_life"
    )

    url_button_2: InlineKeyboardButton = InlineKeyboardButton(
        text="Где то тут я учусь",
        url="https://stepik.org/12092"
    )

    url_button_3: InlineKeyboardButton = InlineKeyboardButton(
        text="Мой телеграм канал еще раз",
        url="tg://resolve?domain=nickwiden_life"
    )

    # Создаем список списков с кнопками
    keyboard: list[list[InlineKeyboardButton]] = [
        [url_button_1, url_button_2],
        [url_button_3]
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


@dp.message()
async def send_echo(message: Message):
    await message.answer(text='Это бот для тестов, привет)')


if __name__ == '__main__':
    dp.run_polling(bot)
