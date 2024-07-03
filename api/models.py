from django.db import models


# Create your models here.
class Problem(models.Model):
    idDisplay = models.CharField(max_length=10, unique=True)

    title = models.TextField()
    description = models.TextField()
