from django.db import models


class Problem(models.Model):
    id = models.CharField(max_length=10, primary_key=True)

    title = models.CharField(max_length=256)
    description = models.TextField()

    level = models.IntegerField(default=1)
