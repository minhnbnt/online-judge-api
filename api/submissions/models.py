from uuid import uuid4

from django.db import models
from django.contrib.auth import get_user_model

from api.models import Problem


# Create your models here.
class Submission(models.Model):
    owner = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    viewId = models.UUIDField(default=uuid4, editable=False)
    summittedOn = models.DateTimeField(auto_now_add=True)

    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    language = models.CharField(max_length=20)
    version = models.CharField(max_length=10)
    source = models.TextField()

    judgeResult = models.CharField(max_length=3)
    errorLogs = models.TextField(null=True)
