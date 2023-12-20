from django.urls import path
from .views import TaskListApiView, TaskDetailApiView, SubtaskView, SubtaskViewDetail

urlpatterns = [
  path('',  TaskListApiView.as_view(), name="tasks-list"),
  path('<int:pk>/', TaskDetailApiView.as_view(), name="tasks-details"),
  path('subtasks/', SubtaskView.as_view(), name="subtasks-list"),
  path('subtasks/<int:pk>/', SubtaskViewDetail.as_view(), name="subtask-detail")
]
