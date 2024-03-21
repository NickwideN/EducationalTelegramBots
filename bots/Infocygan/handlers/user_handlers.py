from aiogram import Router, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery

from lexicon.lexicon import get_text
from keyboards.keyboards import create_inline_kb

router = Router()


@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer_video('BAACAgQAAxkBAAMDZfibvYKr0Qr21lgmFjA4IDpPQHYAAgIFAALX2lRTwOCACFhU2vs0BA',
                               caption=get_text('/start'),
                               reply_markup=create_inline_kb(1, 'start_polling', 'cancel_polling'))


@router.callback_query(F.data.in_(["cancel_polling", "start_polling"]))
async def process_callback1(callback: CallbackQuery):
    await callback.message.answer_photo(
        'AgACAgQAAxkBAAMEZfibvaYkpGwg6Q9oioJJlNVZB8oAAnizMRvi20RTYbOLr93WCXIBAAMCAAN3AAM0BA',
        caption=get_text('went_to_bank'),
        reply_markup=create_inline_kb(1, 'go_to_bank'))
    await callback.answer()


@router.callback_query(F.data == 'go_to_bank')
async def process_callback2(callback: CallbackQuery):
    await callback.message.answer(text='Только что вы увидели демонстрацию работы бота. '
                                       'Естественно, содержание бота можно будет изменить')
    await callback.answer()
   