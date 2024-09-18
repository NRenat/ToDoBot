from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics

from ToDoBot_API.filters import TaskFilter
from ToDoBot_API.models import Task, UserFromTelegram
from ToDoBot_API.serializers import TaskSerializer, UserFromTelegramSerializer


class TaskView(generics.ListCreateAPIView, generics.UpdateAPIView,
               generics.RetrieveAPIView):
    queryset = Task.objects.select_related('author').prefetch_related('categories')
    serializer_class = TaskSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TaskFilter
    lookup_field = 'id'


class UserFromTelegramView(generics.ListCreateAPIView):
    queryset = UserFromTelegram.objects.all()
    serializer_class = UserFromTelegramSerializer
