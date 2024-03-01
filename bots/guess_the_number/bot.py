import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from config_reader import env
from user import get_user

bot = Bot(token=env('BOT_TOKEN'))
dp = Dispatcher()

ATTEMPT_LIMIT = 5


@dp.message(CommandStart())
async def process_start(message: Message):
    await message.answer('Привет. Давай поиграем в игру "Угадай число"!\n'
                         'Чтобы узнать правила игры и список доступных команд, отправьте команду /help')


@dp.message(Command('help'))
async def process_help(message: Message):
    await message.answer(f'Правила игры:\n\n'
                         f'Я загадываю число от 1 до 100, а вам нужно его угадать\n'
                         f'У вас есть {ATTEMPT_LIMIT} попыток\n\n'
                         f'Доступные команды:\n'
                         f'/help - правила игры и список команд\n'
                         f'/cancel - выйти из игры\n'
                         f'/stat - посмотреть статистику\n\n'
                         f'Давай сыграем?'
                         )


@dp.message(Command('stat'))
async def process_stat(message: Message):
    user = get_user(message.from_user.id)
    await message.reply(f'Всего сыграно - {user.total_games}\n'
                        f'Побед - {user.wins}')


@dp.message(Command('cancel'))
async def process_cancel(message: Message):
    user = get_user(message.from_user.id)
    if user.in_game:
        user.in_game = False
        await message.answer('Вы вышли из игры. Если захотите сыграть снова, напишите об этом')
    else:
        await message.answer('А мы и так не играем. Может сыграем разок?)')


@dp.message(F.text.lower().in_(['давай', 'да', 'сыграем', 'игра', 'играть', 'хочу играть', 'хочу поиграть',
                                'давай играть']))
async def process_positive_answer(message: Message):
    user = get_user(message.from_user.id)
    if user.in_game:
        await message.answer('Пока мы в игре, я могу реагировать только на числа от 1 до 100 и команды'
                             ' /cancel и /stat')
    else:
        user.in_game = True
        user.attempts = ATTEMPT_LIMIT
        user.secret_number = random.randint(1, 100)
        await message.answer(f'Хорошо! Я загадал число от 1 до 100.\n'
                             f'У тебя есть {ATTEMPT_LIMIT} попыток, чтобы его отгадать')


@dp.message(F.text.lower().in_(['не', 'нет', 'не буду', 'не хочу']))
async def process_negative_answer(message: Message):
    user = get_user(message.from_user.id)
    if user.in_game:
        await message.answer('Пока мы в игре, я могу реагировать только на числа от 1 до 100 и команды'
                             ' /cancel и /stat')
    else:
        await message.answer(f'Ладно☹️\n\n'
                             f'Если захотите поиграть, просто напишите об этом')


@dp.message(lambda message: message.text and message.text.isdigit() and 1 <= int(message.text) <= 100)
async def process_number_answer(message: Message):
    user = get_user(message.from_user.id)
    if user.in_game:
        user.attempts -= 1
        if int(message.text) == user.secret_number:
            user.in_game = False
            user.total_games += 1
            user.wins += 1
            await message.answer('Поздравляю! Вы угадали число!\n\nМожет сыграем снова?;)')
        elif user.attempts == 0:
            user.in_game = False
            user.total_games += 1
            await message.answer(f'Это была последняя попытка.\n\n'
                                 f'Вы проиграли! Я загадал число {user.secret_number}.'
                                 f'Давайте сыграем еще и проверим ваши навыки гадалки🧐')
        elif int(message.text) > user.secret_number:
            await message.answer('Мое число меньше')
        elif int(message.text) < user.secret_number:
            await message.answer('Мое число больше')
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')


@dp.message()
async def process_other_answers(message: Message):
    user = get_user(message.from_user.id)
    if user.in_game:
        await message.answer(
            'Мы же сейчас с вами играем. '
            'Присылайте, пожалуйста, числа от 1 до 100'
        )
    else:
        await message.answer(
            'Таких понятий я не понимаю, давай просто поиграем😉'
        )


if __name__ == "__main__":
    dp.run_polling(bot)
