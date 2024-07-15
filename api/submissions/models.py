from uuid import uuid4

from django.db import models
from django.db.utils import settings

from api.models import Problem


# Create your models here.
class Submission(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    secret = models.UUIDField(default=uuid4, editable=False)

    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

    language = models.CharField(max_length=20)
    version = models.CharField(max_length=10)
    source = models.TextField()

    judgeResult = models.CharField(max_length=3)
    errorLogs = models.TextField(null=True)
