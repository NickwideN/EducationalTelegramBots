import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config_data.config import Config, load_config
import handlers
from handlers.other import router as other_router
from handlers.user import router as user_router
from middlewares.inner import (
    FirstInnerMiddleware,
    SecondInnerMiddleware,
    ThirdInnerMiddleware,
)
from middlewares.outer import (
    FirstOuterMiddleware,
    SecondOuterMiddleware,
    ThirdOuterMiddleware,
)

# Настраиваем базовую конфигурацию логгирования
logging.basicConfig(level=logging.DEBUG,
                    format='[{asctime}] {filename}:{lineno}  #{levelname:8} - {message}',
                    style='{')

# Инициализируем логгер модуля
logger = logging.getLogger(__name__)

async def main():
    logger.info('Starting Bot')
    config: Config = load_config()

    bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(
        parse_mode='HTML',
    ))
    dp = Dispatcher()

    # регистрируем роутеры

    dp.include_routers(*handlers.routers)

    # Здесь будем регистрировать миддлвари
    dp.update.outer_middleware(FirstOuterMiddleware())
    other_router.message.middleware(SecondOuterMiddleware())


    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
