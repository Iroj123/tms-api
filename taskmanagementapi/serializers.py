from rest_framework import serializers
from django.contrib.auth import get_user_model

from taskmanagementapi.models import Project, Task, UserTask

User = get_user_model()

class ProjectSerializer(serializers.ModelSerializer):
    tasks = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model=Project
        fields=['id','name','description','created_at','updated_at','tasks']




class TaskSerializer(serializers.ModelSerializer):
    assigned_users = serializers.SerializerMethodField()

    class Meta:
        model=Task
        fields=['id','title','description','due_date','status','project','assigned_users']

    def get_assigned_users(self, obj):
        return [user_task.user.first_name for user_task in obj.usertask_set.all()]


class UserTaskSerializer(serializers.ModelSerializer):
    task_details = TaskSerializer(source='task', read_only=True)

    class Meta:
        model=UserTask
        fields=['id','user','task','assigned_date','completed','task_details']


