import os

from aiogram import Bot
from aiogram_dialog import DialogManager
from fluent.runtime import FluentResourceLoader, FluentLocalization


async def error_status_handler(manager: DialogManager, response):
    """
    Return false if no error status
    Return true if error status
    """
    if 400 <= response.status_code < 500:
        await smth_wrong_answer(manager)
        return True
    return False


async def smth_wrong_answer(manager: DialogManager):
    l10ns = await get_user_lang(manager)
    smth_wrong_text = l10ns.format_value('smth_wrong_text')
    bot: Bot = manager.middleware_data.get('bot')
    chat_id = manager.event.from_user.id
    await bot.send_message(chat_id, smth_wrong_text)


async def get_user_lang(manager):
    locale = manager.event.from_user.language_code
    l10ns = get_translations(locale)
    return l10ns


async def shorten_text(objects: list, field: str, length: int = 30, ):
    if objects:
        objects = [
            {**obj, field: obj[field][:length] + '...'} if len(
                obj[field]) > length else obj
            for obj in objects
        ]
    else:
        objects = []
    return objects


def get_translations(locale: str):
    loader = FluentResourceLoader(os.path.join(
        os.path.dirname(__file__),
        'translations',
        '{locale}',
    ))
    l10ns = FluentLocalization(
        [locale, 'en'], ['main.ftl'], loader
    )
    return l10ns
