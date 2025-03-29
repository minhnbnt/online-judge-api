from django.db import models
from api.users.models import User


class Problem(models.Model):
    id = models.CharField(max_length=10, primary_key=True)

    title = models.CharField(max_length=256)
    description = models.TextField()

    level = models.IntegerField(default=1)

    stdin = models.TextField(default="")
    stdout = models.TextField(blank=False)

    runFlags = models.TextField(null=True)

    timeLimit = models.IntegerField(null=True)
    memoryLimit = models.IntegerField(null=True)


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    comment = models.TextField(blank=False)
    commentedOn = models.DateTimeField(auto_now_add=True)
