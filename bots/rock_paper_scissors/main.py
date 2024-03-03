import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from config_data.config import Config, load_config
from handlers import other_handlers, user_handlers

# Initialize logger
logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(level=logging.INFO,
                        format='{filename}:{lineno} [{asctime}] #{levelname:8} - {name} - {message}',
                        style='{'
                        )

    logger.info('Starting Bot')

    config: Config = load_config()
    bot: Bot = Bot(token=config.tg_bot.token, default=DefaultBotProperties(parse_mode='HTML'))
    dp = Dispatcher()

    dp.include_routers(user_handlers.router, other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
