from django.urls import path, include
from rest_framework .routers import DefaultRouter

from taskmanagementapi.viewset import TaskViewSet, ProjectTaskViewSet, TaskDetailViewSet, ProjectTasksView

router = DefaultRouter()
router.register('tasks',TaskViewSet)
router.register('users',TaskDetailViewSet)
router.register('project',ProjectTaskViewSet)


urlpatterns = [
    path('',include(router.urls)),
    path('project/<int:project_id>/tasks/',ProjectTasksView.as_view(),name='project-tasks'),

]