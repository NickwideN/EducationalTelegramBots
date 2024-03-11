import logging

from aiogram import Router, Dispatcher
from aiogram.types import Message

from lexicon.lexicon import LEXICON
from filters.filters import MyTrueFilter
from middlewares.outer import SecondOuterMiddleware

router = Router()


logger = logging.getLogger(__name__)


# Этот хэндлер будет срабатывать на любые сообщения,
# кроме тех, для которых есть отдельные хэндлеры
@router.message(MyTrueFilter())
async def send_echo(message: Message):
    logger.debug('Вошли в эхо-хэндлер')
    await message.reply(text=LEXICON['other_answer'])
    logger.debug('Выходим из эхо-хэндлера')


