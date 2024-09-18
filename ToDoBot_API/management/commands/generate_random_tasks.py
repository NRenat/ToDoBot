from datetime import timedelta
import random

import requests
from django.utils import timezone
from django.core.management.base import BaseCommand
from ToDoBot_API.models import Task, UserFromTelegram, Category


class Command(BaseCommand):
    help = 'Generate random tasks using JsonPlaceholder and create some categories'

    def handle(self, *args, **kwargs):
        response = requests.get('https://jsonplaceholder.typicode.com/todos')
        if response.status_code != 200:
            self.stderr.write('Failed to fetch data from JsonPlaceholder')
            return

        tasks_data = response.json()

        users = UserFromTelegram.objects.all()

        if not users:
            self.stderr.write('No users found in the database.')
            return

        category_names = ('Work', 'Personal', 'Urgent', 'Miscellaneous')
        categories = {}
        for name in category_names:
            category, created = Category.objects.get_or_create(name=name)
            categories[name] = category
            if created:
                self.stdout.write(f'Created category: {name}')

        for task_data in tasks_data:
            user = users.order_by('?').first()
            due_date = timezone.now() + timedelta(days=random.randint(1, 365))

            task, created = Task.objects.get_or_create(
                title=task_data['title'],
                defaults={
                    'author': user,
                    'description': task_data['title'],
                    'completed': task_data['completed'],
                    'due_date': due_date
                }
            )

            if created:
                category = list(categories.values())[0]
                task.categories.add(category)
                self.stdout.write(f'Created task: {task.title}')
            else:
                self.stdout.write(f'Task already exists: {task.title}')
