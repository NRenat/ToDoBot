from datetime import datetime, date
from typing import Any

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import (
    Next, Calendar, Row, Button, ScrollingGroup, Select
)
from aiogram_dialog.widgets.text import Format

from i18n_format import I18NFormat
from internal_requests.service import api_service
from states import CreateTaskSG, DialogSG
from utils import get_user_lang, shorten_text, error_status_handler


async def get_task_review_data(dialog_manager: DialogManager, **kwargs):
    data = dialog_manager.current_context().widget_data

    l10ns = await get_user_lang(dialog_manager)
    title = l10ns.format_value('task_details_title',
                               {'title': data.get('title', 'N/A')})
    description = l10ns.format_value('task_details_description', {
        'description': data.get('description', 'N/A')})
    categories = l10ns.format_value('task_details_categories', {
        'categories': data.get('categories', 'N/A')})
    due_date = l10ns.format_value(
        'task_details_due_date',
        {'due_date': data.get('deadline', 'N/A')}
    )

    formatted_text = (
        f'{title}\n\n{description}\n\n{categories}\n\n{due_date}'
    )
    return {
        'task_details': formatted_text
    }


async def on_save_task(callback: CallbackQuery, button: Button, manager: DialogManager):
    data = manager.current_context().widget_data
    task_data = {
        'title': data.get('title'),
        'description': data.get('description'),
        'categories': data.get('categories').strip().split(','),
        'due_date': data.get('deadline'),
        'author': manager.event.from_user.id,
    }
    response = await api_service.create_task(task_data)
    if await error_status_handler(manager, response):
        await manager.done()
    else:
        l10ns = await get_user_lang(manager)
        created_task_text = l10ns.format_value('created-task', )
        await callback.message.answer(created_task_text)
        await manager.done()


async def get_data(dialog_manager: DialogManager, **kwargs):
    user_id = dialog_manager.event.from_user.id
    response = await api_service.get_tasks(user_id)
    if await error_status_handler(dialog_manager, response):
        await dialog_manager.done()
    else:
        tasks = response.json()
        tasks = await shorten_text(tasks, field='title')
        return {
            'tasks': tasks
        }


async def on_task_selected(callback: CallbackQuery, widget: Any,
                           manager: DialogManager, item_id: str):
    await manager.start(DialogSG.task_view, data={'task_id': item_id})


async def get_task_data(dialog_manager: DialogManager, **kwargs):
    context = dialog_manager.current_context()
    task_id = context.start_data.get('task_id')
    if not task_id:
        return {'task_details': 'Task ID not found!'}

    response = await api_service.get_task_details(task_id)

    if await error_status_handler(dialog_manager, response):
        await dialog_manager.done()
    else:
        task_details = response.json()[0]

        l10ns = await get_user_lang(dialog_manager)
        title = l10ns.format_value('task_details_title',
                                   {'title': task_details.get('title', 'N/A')})
        description = l10ns.format_value("task_details_description", {
            'description': task_details.get('description', 'N/A')})
        categories = l10ns.format_value("task_details_categories", {
            'categories': ', '.join(task_details.get('categories', []))
        })
        created_date = l10ns.format_value('task_details_created_date',
                                          {'created_date': await format_date(
                                              task_details.get('created_date'))})
        due_date = l10ns.format_value('task_details_due_date',
                                      {'due_date': await format_date(
                                          task_details.get('due_date'))})

        formatted_text = (
            f'{title}\n\n{description}\n\n{categories}\n\n{created_date}\n\n{due_date}'
        )

        return {
            'task_details': formatted_text
        }


async def on_date_selected(callback: CallbackQuery, widget,
                           dialog_manager: DialogManager, selected_date: date):
    data = dialog_manager.current_context().widget_data
    data['deadline'] = str(selected_date)
    await dialog_manager.switch_to(CreateTaskSG.confirm)


async def close_task(callback: CallbackQuery, button: Button,
                     dialog_manager: DialogManager, ):
    task_id = dialog_manager.current_context().start_data.get('task_id')
    response = await api_service.close_task(task_id)
    await error_status_handler(dialog_manager, response)
    await dialog_manager.done()


async def get_comments_data(dialog_manager: DialogManager, **kwargs):
    task_id = dialog_manager.current_context().start_data.get('task_id')
    response = await api_service.get_comments(
        task_id)
    if await error_status_handler(dialog_manager, response):
        await dialog_manager.done()
    else:
        comments = response.json()
        comments = await shorten_text(comments, field='text')
        return {
            'comments': comments
        }


async def delete_comment(callback: CallbackQuery, widget: Any,
                         dialog_manager: DialogManager):
    comment_id = dialog_manager.dialog_data['comment_id']
    task_id = dialog_manager.start_data['task_id']
    response = await api_service.delete_comment(task_id, comment_id)
    if await error_status_handler(dialog_manager, response):
        await dialog_manager.switch_to(DialogSG.view_comments)
    else:
        l10ns = await get_user_lang(dialog_manager)
        deleted_comment_text = l10ns.format_value('deleted-comment', )
        await callback.message.answer(deleted_comment_text)
        await dialog_manager.switch_to(DialogSG.view_comments)


async def get_comment_data(dialog_manager: DialogManager, **kwargs):
    task_id = dialog_manager.start_data['task_id']
    comment_id = dialog_manager.dialog_data['comment_id']
    response = await api_service.get_comment(task_id, comment_id)
    if await error_status_handler(dialog_manager, response):
        await dialog_manager.done()
    else:
        comment = response.json()
        return {'comment-detail': comment['text']}


async def on_comment_selected(callback: CallbackQuery, widget: Any,
                              manager: DialogManager, item_id: str):
    manager.dialog_data['comment_id'] = item_id
    await manager.switch_to(
        DialogSG.view_comment)


async def comment_handler(message: Message, message_input: MessageInput,
                          dialog_manager: DialogManager):
    context = dialog_manager.current_context()
    task_id = context.start_data['task_id']
    new_comment = message.text
    response = await api_service.add_comment(task_id, new_comment)
    if await error_status_handler(dialog_manager, response):
        await dialog_manager.done()
    else:
        await dialog_manager.switch_to(DialogSG.view_comments)


create_dialog = Dialog(
    Window(
        I18NFormat('Enter-Title'),
        TextInput(id='title', on_success=Next()),
        state=CreateTaskSG.title,
    ),
    Window(
        I18NFormat('Enter-Description'),
        TextInput(id='description', on_success=Next()),
        state=CreateTaskSG.description,
    ),
    Window(
        I18NFormat('Enter-Category'),
        TextInput(id='categories', on_success=Next()),
        state=CreateTaskSG.categories,
    ),
    Window(
        I18NFormat('Enter-Deadline:'),
        Calendar(
            id='due_date',
            on_click=on_date_selected,
        ),
        state=CreateTaskSG.due_date
    ),
    Window(
        I18NFormat('{task_details}').text,
        Row(
            Button(I18NFormat('Save'), id='save_task', on_click=on_save_task),
        ),
        state=CreateTaskSG.confirm,
        getter=get_task_review_data
    ),
)

menu_dialog = Dialog(
    Window(
        I18NFormat('Tasks-list'),
        ScrollingGroup(
            Select(
                Format('{item[title]}'),
                id='tasks_list',
                items='tasks',
                item_id_getter=lambda x: x['id'],
                on_click=on_task_selected,
            ),
            id='tasks_scroll',
            width=1,
            height=5
        ),
        state=DialogSG.menu,
        getter=get_data,
    ),
    Window(
        I18NFormat('{task_details}').text,
        Row(
            Button(I18NFormat('Back'), id='back', on_click=lambda c, b, m: m.back()),
            Button(I18NFormat('Close-Task'), id='close_task', on_click=close_task),
            Button(I18NFormat('Comments'), id='comments',
                   on_click=lambda c, b, m: m.next()),
        ),
        state=DialogSG.task_view,
        getter=get_task_data,
    ),
    Window(
        I18NFormat('Comments:'),
        ScrollingGroup(
            Select(
                Format('{item[text]}'),
                id='comments_list',
                items='comments',
                item_id_getter=lambda x: x.get('id'),
                on_click=on_comment_selected,
            ),
            id='comments_scroll',
            width=1,
            height=5,
        ),
        Row(
            Button(I18NFormat('Back'), id='back_to_task',
                   on_click=lambda c, b, m: m.back()),
            Button(I18NFormat('Add-Comment'), id='add_comment',
                   on_click=lambda c, b, m: m.next()),
        ),
        state=DialogSG.view_comments,
        getter=get_comments_data,
    ),
    Window(
        I18NFormat('Enter-Comment'),
        MessageInput(comment_handler, ),
        Row(
            Button(I18NFormat('Back'), id='back_to_comments',
                   on_click=lambda c, b, m: m.back()),
        ),
        state=DialogSG.add_comment,
    ),
    Window(
        Format('{comment-detail}'),
        TextInput(id='view_comment'),
        Row(
            Button(I18NFormat('Back'), id='back_to_comments',
                   on_click=lambda c, b, m: m.switch_to(DialogSG.view_comments)),
            Button(I18NFormat('Delete'), id='delete_comment', on_click=delete_comment),
        ),
        state=DialogSG.view_comment,
        getter=get_comment_data,
    ),
)


async def format_date(dt: str):
    date_obj = datetime.fromisoformat(dt)
    return date_obj.strftime('%d-%m-%Y')
