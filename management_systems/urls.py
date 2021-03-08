from django.urls import path

from .views import PoolEntranceListView, IndexView, PoolEntranceCreateView, PoolEntranceDeleteView, \
    PoolEntranceUpdateView, NewsCreateView, ArchivePoolEntranceListView, AddTaskCreateView,  close_visit
from .views import TaskListView, change_task_status, TaskDeleteView, TaskAddCommentUpdateView, \
    PendingServicesListView, WorkerWeeklyScheduleListView, complete_service, WorkerDayScheduleCreateView

urlpatterns = [
    path('pool-management/', PoolEntranceListView.as_view(), name='pool-management'),
    path('create-pool-entrance/', PoolEntranceCreateView.as_view(), name='create-pool-entrance'),
    path('delete/<int:pk>/', PoolEntranceDeleteView.as_view(), name='delete-pool-entrance'),
    path('edit-pool-entrance/<int:pk>/', PoolEntranceUpdateView.as_view(), name='edit-pool-entrance'),
    path('create-news/', NewsCreateView.as_view(), name='create-news'),
    path('close-visit/<int:pk>/', close_visit, name='close-visit'),
    path('change-task-status/<int:pk>', change_task_status, name='change_task_status'),
    path('complete-service/<int:pk>/', complete_service, name='complete-service'),
    path('archive-visits/', ArchivePoolEntranceListView.as_view(), name='archive-visits'),
    path('create-task/', AddTaskCreateView.as_view(), name='create-task'),
    path('task-list/', TaskListView.as_view(), name='task-list'),
    path('delete-task/<int:pk>/', TaskDeleteView.as_view(), name='delete-task'),
    path('add-task-comment/<int:pk>/', TaskAddCommentUpdateView.as_view(), name='add-task-comment'),
    path('pending-services/', PendingServicesListView.as_view(), name='pending-services'),
    path('weekly-schedule/', WorkerWeeklyScheduleListView.as_view(), name='weekly-schedule'),
    path('create-day-schedule/', WorkerDayScheduleCreateView.as_view(), name='create-day-schedule'),
    path('home/', IndexView.as_view(), name='home')
]