import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from fluentogram import TranslatorHub

import config_data

# Настраиваем базовую конфигурацию логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='[{asctime}] #{levelname:8} {filename}:'
           '{lineno} - {name} - {message}',
    style='{'
)

# Инициализируем логгер модуля
logger = logging.getLogger(__name__)

# Функция конфигурирования и запуска бота
async def main() -> None:

    # Загружаем конфиг в переменную config
    config: config_data.Config = config_data.load_config()

    bot = Bot(
        token=config.tg_bot.token,
        default=DefaultBotProperties(parse_mode='HTML'),
    )

    dp = Dispatcher()






asyncio.run(main())