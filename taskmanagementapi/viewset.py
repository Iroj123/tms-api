from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from taskmanagementapi.models import Task, Project, UserTask
from taskmanagementapi.permissions import IsAdmin, IsManager, IsOwnerOrReadOnly
from taskmanagementapi.serializers import TaskSerializer, ProjectSerializer, UserTaskSerializer


class ProjectTaskViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdmin | IsManager]

    def perform_create(self, serializer):
        serializer.save()

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    Permission_class=[IsAdmin | IsManager | IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

class TaskDetailViewSet(viewsets.ModelViewSet):
    queryset = UserTask.objects.all()
    serializer_class = UserTaskSerializer
    permission_classes = [IsAdmin | IsManager|IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save()

    def perform_update(self, serializer):
        user_task=self.get_object()
        user_task.completed= self.request.data.get('completed',user_task.completed)
        user_task.save()
        return Response(UserTaskSerializer(user_task).data,status=status.HTTP_200_OK)

class ProjectTasksView(APIView):
    permission_classes = [permissions.IsAuthenticated]


    def get(self, request, project_id, format=None):
        tasks = Task.objects.filter(project_id=project_id)
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)



