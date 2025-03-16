from aiogram import Router
from aiogram.types import Message
from fluentogram import TranslatorRunner

# Инициализируем роутер уровня модуля
router = Router()

# Этот хэндлер будет срабатывать на любые сообщения и
# отправлять пользователю их копию
@router.message()
async def send_echo(message: Message, i18n: TranslatorRunner):
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text=i18n.get('no-copy'))