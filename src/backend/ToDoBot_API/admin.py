from django.contrib import admin

from ToDoBot_API.models import Task, Category, UserFromTelegram


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'completed', 'author', 'created_date',)
    list_filter = ('completed', 'author',)
    search_fields = ('title',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(UserFromTelegram)
class UserFromTelegramAdmin(admin.ModelAdmin):
    list_display = ('telegram_id',)
    list_filter = ('telegram_id',)
    search_fields = ('telegram_id',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('text',)
    list_filter = ('text',)
    search_fields = ('text',)