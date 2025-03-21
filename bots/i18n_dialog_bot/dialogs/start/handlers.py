from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button
from fluentogram import TranslatorRunner


async def button_click(
        callback: CallbackQuery,
        button: Button,
        dialog_manager: DialogManager
) -> None:
    i18n: TranslatorRunner = dialog_manager.middleware_data.get('i18n')
    await callback.answer(text=i18n.get('button-pressed'))