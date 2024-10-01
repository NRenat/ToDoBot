from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from internal_requests.service import api_service
from states import CreateTaskSG, DialogSG
from utils import get_translations

router = Router()


@router.message(Command('new'))
async def new_task_handler(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(CreateTaskSG.title, mode=StartMode.RESET_STACK)


@router.message(Command('menu'))
async def menu(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(DialogSG.menu, mode=StartMode.RESET_STACK)


@router.message(Command('start'))
async def start(message: Message):
    user_tg_id = message.from_user.id
    response = await api_service.create_user(user_tg_id)
    locale = message.from_user.language_code
    l10ns = get_translations(locale)
    if 400 <= response.status_code < 500:
        smth_wrong_text = l10ns.format_value('smth_wrong_text')
        await message.answer(smth_wrong_text)
    welcome_text = l10ns.format_value('welcome-text', )
    await message.answer(welcome_text)
