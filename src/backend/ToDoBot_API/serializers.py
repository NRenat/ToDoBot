from rest_framework import serializers

from ToDoBot_API.models import UserFromTelegram, Category, Task, Comment


class UserFromTelegramSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserFromTelegram
        fields = ('telegram_id',)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)


class TaskSerializer(serializers.ModelSerializer):
    categories = serializers.ListSerializer(
        child=serializers.CharField(),
        required=False
    )

    class Meta:
        model = Task
        fields = (
            'id', 'title', 'description', 'completed', 'created_date',
            'categories', 'due_date', 'author'
                  )

    def create(self, validated_data):
        categories_data = validated_data.pop('categories', [])
        task = Task.objects.create(**validated_data)
        self._update_categories(task, categories_data)
        return task

    def update(self, instance, validated_data):
        categories_data = validated_data.pop('categories', [])
        instance = super().update(instance, validated_data)
        self._update_categories(instance, categories_data)
        return instance

    def _update_categories(self, task, categories_data):
        category_objects = []
        for category_name in categories_data:
            category, created = Category.objects.get_or_create(name=category_name)
            category_objects.append(category)
        task.categories.set(category_objects)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'text', 'created_date')

