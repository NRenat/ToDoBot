from django.db import models
from ulid import ULID
from ulid_django.models import ULIDField


class Category(models.Model):
    id = ULIDField(primary_key=True, default=ULID, editable=False)
    name = models.CharField(max_length=100, unique=True, verbose_name='Category Name')

    def __str__(self):
        return self.name


class UserFromTelegram(models.Model):
    telegram_id = models.PositiveBigIntegerField(
        verbose_name='Telegram ID',
        unique=True,
        db_index=True,
        primary_key=True,
    )
    LANGUAGE_CHOICES = (
        ('en', 'English'),
        ('ru', 'Russian'),
    )
    language = models.CharField(max_length=2, default='en', verbose_name='Language',
                                choices=LANGUAGE_CHOICES)

    def __str__(self):
        return f'TG User ID: {self.telegram_id}'


class Task(models.Model):
    id = ULIDField(primary_key=True, default=ULID, editable=False)
    title = models.CharField(max_length=100, verbose_name="Task Title")
    author = models.ForeignKey(UserFromTelegram, on_delete=models.CASCADE,
                               verbose_name="Task Author")
    description = models.TextField(verbose_name="Task Description")
    completed = models.BooleanField(default=False, verbose_name="Completed")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
    categories = models.ManyToManyField(Category, related_name='tasks',
                                        verbose_name="Categories")
    due_date = models.DateTimeField(null=True, blank=True, verbose_name="Due Date")

    def __str__(self):
        return self.title


class Comment(models.Model):
    id = ULIDField(primary_key=True, default=ULID, editable=False)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments",
                             verbose_name="Task")
    text = models.TextField(verbose_name="Comment Text")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")

    def __str__(self):
        return self.text[:30]
