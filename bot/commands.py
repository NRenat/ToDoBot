import os

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from internal_requests.service import api_service
from states import CreateTaskSG, DialogSG

router = Router()


@router.message(Command("new"))
async def new_task_handler(message: Message, dialog_manager: DialogManager):
    await auth()
    await dialog_manager.start(CreateTaskSG.title, mode=StartMode.RESET_STACK)


@router.message(Command("menu"))
async def menu(message: Message, dialog_manager: DialogManager):
    await auth()
    await dialog_manager.start(DialogSG.menu, mode=StartMode.RESET_STACK)


@router.message(Command("start"))
async def start(message: Message):
    await auth()
    user_tg_id = message.from_user.id
    await api_service.create_user(user_tg_id)
    await message.answer(
        "Welcome to the bot! Use /menu to view tasks.\n/new to create a new task"
        "\n\nДобро пожаловать! Используйте /menu, чтобы открыть список задач.\n/new,"
        " чтобы создать новую задачу")


async def auth():
    await api_service.authenticate(username=os.getenv('BOT_BACK_USER'),
                                   password=os.getenv('BOT_BACK_PASS'))
