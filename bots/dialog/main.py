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


# Хэндлер, обрабатывающий нажатие на кнопку 'Да'
async def yes_click_process(callback: CallbackQuery,
                            widget: Button,
                            dialog_manager: DialogManager):
    await callback.message.edit_text(
        text='<b>Прекрасно!</b>\n\nНадеюсь, вы найдете в этом курсе что-то '
             'новое и полезное для себя!'
    )
    await dialog_manager.done()


# Хэндлер, обрабатывающий нажатие на кнопку 'Нет'
async def no_click_process(callback: CallbackQuery,
                           widget: Button,
                           dialog_manager: DialogManager):
    await callback.message.edit_text(
        text='<b>Попробуйте!</b>\n\nСкорее всего, вам понравится!'
    )
    await dialog_manager.done()


async def username_getter(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    return {'username': event_from_user.username}


async def get_name(dialog_manager: DialogManager, event_from_user: User, **kwargs):
    return {'namr': event_from_user.first_name or 'Странник'}


async def get_number(**kwargs):
    return {'number': random.randint(1, 3)}


async def get_items(**kwargs):
    return {'items': (
        (1, 'Пункт 1'),
        (2, 'Пункт 2'),
        (3, 'Пункт 3'),
    )}


async def button_clicked(callback: CallbackQuery, button: Button, manager: DialogManager):
    await callback.message.answer('Кажется, ты нажал на кнопку!')


# Это хэндлер, обрабатывающий нажатие инлайн-кнопок
async def button_when_clicked(callback: CallbackQuery, button: Button, dialog_manager: DialogManager):
    another_button = dialog_manager.dialog_data.get('another_button')
    dialog_manager.dialog_data.update(another_button=not another_button)


# Это геттер
async def get_button_when_status(dialog_manager: DialogManager, **kwargs):
    another_button = dialog_manager.dialog_data.get('another_button')
    return {'button_status': another_button}


async def get_photo(**kwargs):
    image = MediaAttachment(ContentType.PHOTO, url="http://teoria.on.ge/files/new/f24b95a352dc25441ea2b32cb823623b.jpg")
    return {'photo': image}


class StartSG(StatesGroup):
    start_const = State()
    start_format = State()
    start_with_buttons = State()
    start_multi = State()
    start_case = State()
    start_list = State()
    start_button = State()
    start_when = State()
    start_test = State()


# Это стартовый диалог
start_dialog = Dialog(
    Window(
        Const(text='Привет! Это простой диалог на aiogram_dialog.'),
        state=StartSG.start_const,
    ),
    Window(
        Format(text='Привет, {username}, это диалог format'),
        state=StartSG.start_format,
        getter=username_getter,
    ),
    Window(
        Format(text='Привет, <b>{username}</b>!\n'),
        Const(
            text='Пробовали ли вы уже писать ботов с использованием '
                 'библиотеки <code>aiogram_dialog</code>?'
        ),
        Row(
            Button(text=Const('✅ Да'), id='yes', on_click=yes_click_process),
            Button(text=Const('✖️ Нет'), id='no', on_click=no_click_process),
        ),
        getter=username_getter,
        state=StartSG.start_with_buttons,
    ),
    Window(
        Multi(
            Format('Привет, {name}!'),
            Const('Это демонстрационный пример работы виджета <code>Multi</code>'),
            Const('В этом сообщении внутри виджета <code>Multi</code> один виджет '
                  '<code>Format</code> и два <code>Const</code>'),
            sep='\n\n'
        ),
        getter=get_name,
        state=StartSG.start_multi,
    ),
    Window(
        Case(
            texts={
                1: Const('Это первый текст'),
                2: Const('Это второй текст'),
                3: Const('Это третий текст'),
                ...: Const('Это текст для любого числа'),
            },
            selector='number',
        ),
        getter=get_number,
        state=StartSG.start_case,
    ),
    Window(
        List(field=Format('{item[0]}. {item[1]}'),
             items='items',
             page_size=2),
        getter=get_items,
        state=StartSG.start_list,
    ),
    Window(
        Const('Это сообщение с инлайн-кнопкой. На кнопку можно нажать, '
              'и появится какой-то текст'),
        Button(
            text=Const('Нажми'),
            id='button_1',
            on_click=button_clicked),
        state=StartSG.start_button,
    ),
    Window(
        Const('На кнопки из этого сообщения можно нажать!'),
        Button(
            text=Const('Нажми меня!'),
            id='button_1',
            on_click=button_when_clicked),
        Button(
            text=Const('И меня нажми!'),
            id='button_2',
            on_click=button_when_clicked,
            when='button_status'),
        Url(text=Const('Перейти'),
            url=Const('https://stepik.org/a/153850'),
            id='button_2'),
        state=StartSG.start_when,
        getter=get_button_when_status,
    ),
    Window(
        StaticMedia("photo"),
        state=StartSG.start_test,
        getter=get_photo,
    ),
)


class SG(StatesGroup):
    main = State()
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
        Const("Click find products to show a list of available products:"),
        SwitchTo(Const("Find products"), id="search", state=SG.result),
        state=SG.main,
    ),
    Window(
        Const("Searching results:", when=success),
        Const("Search did not return any results", when=fail),
        ListGroup(
            Url(
                Format("{item[name]} ({item[category]})"),
                Format("{item[url]}"),
                id="url",
            ),
            id="select_search",
            item_id_getter=lambda item: item["id"],
            items="products",
        ),
        Back(Const("Back")),
        state=SG.result,
        getter=actions,
    )
)


# Этот классический хэндлер будет срабатывать на команду /start
@dp.message(CommandStart())
async def command_start_process(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start_test, mode=StartMode.RESET_STACK)


dp.include_router(start_dialog)
dp.include_router(dialog)
setup_dialogs(dp)
dp.run_polling(bot)
