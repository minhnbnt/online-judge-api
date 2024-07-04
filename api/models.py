from django.db import models


# Create your models here.
class Problem(models.Model):
    idDisplay = models.CharField(max_length=10, unique=True)

    title = models.CharField(max_length=256)
    description = models.TextField()

    level = models.IntegerField(default=1)
