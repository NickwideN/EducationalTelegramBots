import asyncio
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

from config_reader import config

# Создаем объекты бота и диспетчера
bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help', 'r']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )


@dp.message(Command('sendTanya'))
async def process_help_command(message: Message):
    await bot.send_message(chat_id='-1002083916526',
                           text=f'From: {message.from_user.username}\n'
                                f'Text: {message.text}\n'
                                f'\u2764\ufe0f'
                           )
    await bot.send_message(chat_id='223370456',
                           text='Привет, я веселый бот! Давай дружить)) \n'
                                '/be_friends'
                           )


@dp.message(Command('be_friends'))
async def process_help_command(message: Message):
    await bot.send_message(chat_id='-1002083916526',
                           text=f'From: {message.from_user.username}\n'
                                f'Text: {message.text}'
                           )
    await message.answer(
        'Ураа:) Теперь мы друзья! \u2764\ufe0f'
    )


# Этот хэндлер будет срабатывать на любые ваши текстовые сообщения,
# кроме команд "/start" и "/help"
@dp.message()
async def send_echo(message: Message):
    await message.reply(text=message.text)


if __name__ == '__main__':
    dp.run_polling(bot)
