from typing import TYPE_CHECKING

from aiogram import F, Router, html
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)
from fluentogram import TranslatorRunner

if TYPE_CHECKING:
    from locales.stub import TranslatorRunner

# Инициализируем роутер уровня модуля
router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message, i18n: TranslatorRunner):
    # username = html.quote(message.from_user.full_name)
    username = message.from_user.mention_html()
    # Создаем объект инлайн-кнопки
    button = InlineKeyboardButton(
        text=i18n.button.button(),
        callback_data='button_pressed'
    )
    # Создаем объект инлайн-клавиатуры
    markup = InlineKeyboardMarkup(inline_keyboard=[[button]])
    # Отправляем сообщение пользователю
    await message.answer(
        text=i18n.hello.user(username=username),
        reply_markup=markup
    )


# Этот хэндлер срабатывает на нажатие инлайн-кнопки
@router.callback_query(F.data == 'button_pressed')
async def process_button_click(callback: CallbackQuery, i18n: TranslatorRunner):
    await callback.answer(text=i18n.button.pressed())