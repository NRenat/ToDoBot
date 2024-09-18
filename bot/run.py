import asyncio
import logging
import os.path

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from dotenv import load_dotenv
from fluent.runtime import FluentLocalization, FluentResourceLoader

from commands import start, router
from dialogs import create_dialog, menu_dialog
from i18n_middleware import I18nMiddleware

from aiogram_dialog import (
    setup_dialogs
)

from internal_requests.service import api_service

load_dotenv()

DEFAULT_LOCALE = "en"
LOCALES = ["en", 'ru']


def make_i18n_middleware():
    loader = FluentResourceLoader(os.path.join(
        os.path.dirname(__file__),
        "translations",
        "{locale}",
    ))
    l10ns = {
        locale: FluentLocalization(
            [locale, DEFAULT_LOCALE], ["main.ftl"], loader,
        )
        for locale in LOCALES
    }
    return I18nMiddleware(l10ns, DEFAULT_LOCALE)


async def on_startup():
    logging.info('Starting authentication')
    await api_service.authenticate(username=os.getenv('BOT_BACK_USER'),
                                   password=os.getenv('BOT_BACK_PASS'))
    logging.info('Authentication complete')
    logging.info('Commands set')


async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=os.getenv("TG_TOKEN"))
    dp = Dispatcher()

    i18n_middleware = make_i18n_middleware()
    dp.message.middleware(i18n_middleware)
    dp.callback_query.middleware(i18n_middleware)

    dp.include_router(router)
    dp.include_router(create_dialog)
    dp.include_router(menu_dialog)
    dp.message.register(start, CommandStart())
    setup_dialogs(dp)
    await on_startup()

    await dp.start_polling(bot,)


if __name__ == '__main__':
    asyncio.run(main())
