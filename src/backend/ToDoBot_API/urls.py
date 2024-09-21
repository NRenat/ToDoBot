from django.conf import settings
from django.urls import path, register_converter
from ulid_django.converters import ULIDConverter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from ToDoBot_API import views
from ToDoBot_API.views import CommentView, CommentViewSet

register_converter(ULIDConverter, "ulid")

urlpatterns = (
    path(f'{settings.API_V1_PREFIX}/tasks/<ulid:id>/', views.TaskView.as_view(),
         name='task'),
    path(f'{settings.API_V1_PREFIX}/tasks/', views.TaskView.as_view(), name='tasks'),
    path(f'{settings.API_V1_PREFIX}/tasks/<ulid:id>/comments/<ulid:comment_id>/',
         CommentView.as_view(), name='task-comment'),
    path(f'{settings.API_V1_PREFIX}/tasks/<ulid:id>/comments/',
         CommentViewSet.as_view(),
         name='task-comments'),
    path(f'{settings.API_V1_PREFIX}/users/', views.UserFromTelegramView.as_view(),
         name='user-create'),
    path(f'{settings.API_V1_PREFIX}/token/', TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path(f'{settings.API_V1_PREFIX}/token/refresh/', TokenRefreshView.as_view(),
         name='token_refresh'),

)
