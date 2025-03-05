from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message

from config_reader import env

# Создаем объекты бота и диспетчера
bot = Bot(token=env('BOT_TOKEN'))
dp = Dispatcher()


# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer('Привет!\nМеня зовут Эхо-бот!\nНапиши мне что-нибудь')


# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer(
        'Напиши мне что-нибудь и в ответ '
        'я пришлю тебе твое сообщение'
    )


@dp.message(F.text == 'привет')
async def send_f(message: Message):
    print((~F.text)())
    await message.reply(text='Зашли в send_f')


@dp.message()
async def send_echo(message: Message):
    try:
        print(f'update_id: {message.message_id}')
        await message.send_copy(chat_id=message.chat.id)
        await message.answer(f'Привет, {message.from_user.first_name} - ID - {message.from_user.id}!')
    except TypeError:
        await message.reply(text='Произошла ошибка. Метод send_copy не работает с таким типом данных')


if __name__ == '__main__':
    print('Бот запущен...')
    dp.run_polling(bot)
