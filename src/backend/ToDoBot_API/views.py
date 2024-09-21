from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.response import Response

from ToDoBot_API.filters import TaskFilter
from ToDoBot_API.models import Task, UserFromTelegram, Comment
from ToDoBot_API.serializers import TaskSerializer, UserFromTelegramSerializer, \
    CommentSerializer


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


class CommentViewSet(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        task_id = self.kwargs['id']
        return Comment.objects.filter(task_id=task_id)

    def create(self, request, *args, **kwargs):
        task_id = self.kwargs['id']
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentView(generics.RetrieveAPIView, generics.DestroyAPIView,
                  generics.ListCreateAPIView,):
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_id'
    lookup_field = 'id'

    def get_queryset(self):
        task_id = self.kwargs['id']
        return Comment.objects.filter(task_id=task_id)

    def create(self, request, *args, **kwargs):
        task_id = self.kwargs['id']
        try:
            task = Task.objects.get(pk=task_id)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(task=task)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
