from pprint import pprint
import random

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode, ContentType
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import CallbackQuery, Message, User
from aiogram_dialog import Dialog, DialogManager, StartMode, Window, setup_dialogs
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiogram_dialog.api.protocols import MediaIdStorageProtocol
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, List, Multi, Case
from aiogram_dialog.widgets.kbd import Button, Row, Url, SwitchTo, ListGroup, Back
from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()


class SG(StatesGroup):
    main = State()
    language = State()
    category = State()
    result = State()


success = F["products"]
fail = ~success


async def actions(**kwargs):
    products = [
        {"id": 1, "name": "Ferrari", "category": "car",
         "url": "https://www.ferrari.com/"},
        {"id": 2, "name": "Detroit", "category": "game",
         "url": "https://wikipedia.org/wiki/Detroit:_Become_Human"},
    ]
    return {
        "products": products,
    }


dialog = Dialog(
    Window(
        Const("Привет! Для изучения ПДД используйте кнопки ниже:"),
        SwitchTo(Const("Билеты"), id="search", state=SG.result),
        SwitchTo(
            text=Const('Change Language'),
            id='language',
            state=SG.language),
        SwitchTo(
            text=Const('Выбрать категорию'),
            id='category',
            state=SG.category),
        state=SG.main,
    ),
)


# Этот классический хэндлер будет срабатывать на команду /start
@dp.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=SG.main, mode=StartMode.RESET_STACK)


dp.include_router(dialog)
setup_dialogs(dp)
dp.run_polling(bot)
