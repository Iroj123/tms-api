from django.contrib.auth import get_user_model
from django.db import models

User=get_user_model()

class Project(models.Model):
    name = models.CharField(max_length=100)
    description=models.TextField(blank=True, null=True)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at= models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name




class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    title=models.CharField(max_length=100)
    description=models.TextField(blank=True, null=True)
    due_date=models.DateTimeField(blank=True, null=True)
    status=models.CharField(max_length=50, choices=STATUS_CHOICES, default='To Do')
    project=models.ForeignKey(Project,on_delete=models.CASCADE,related_name='tasks')

    def __str__(self):
        return self.title

class UserTask(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    task=models.ForeignKey(Task,on_delete=models.CASCADE)
    assigned_date=models.DateTimeField(blank=True, null=True)
    completed=models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.first_name} , {self.task.title}"



