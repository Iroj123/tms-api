from django.contrib import admin
from django.contrib.auth import get_user_model

from taskmanagementapi.models import UserTask, Project, Task

User=get_user_model()

admin.site.register(User)
admin.site.register(Project)
admin.site.register(UserTask)
admin.site.register(Task)
