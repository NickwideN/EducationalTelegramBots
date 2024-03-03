from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from config_reader import env

# Создаем объекты бота и диспетчера
bot = Bot(token=env('BOT_TOKEN'))
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    # Создаем список списков с кнопками
    keyboard: list[list[KeyboardButton]] = [
        [KeyboardButton(text=str(i)) for i in range(1, 4)],
        [KeyboardButton(text=str(i)) for i in range(4, 7)]
    ]

    keyboard.append([KeyboardButton(text='7')])

    # Создаем объект клавиатуры, добавляя в него кнопки
    my_keyboard = ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь', reply_markup=my_keyboard)


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
