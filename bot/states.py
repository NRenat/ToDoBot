from aiogram.fsm.state import StatesGroup, State


class DialogSG(StatesGroup):
    menu = State()
    task_view = State()
    close_task = State()


class CreateTaskSG(StatesGroup):
    title = State()
    description = State()
    categories = State()
    due_date = State()
    confirm = State()
