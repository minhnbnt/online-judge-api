from rest_framework.serializers import ModelSerializer

from .models import Problem


class ProblemDetailSerializer(ModelSerializer):
    class Meta:
        model = Problem
        fields = ["title", "description"]


class ProblemSerializer(ModelSerializer):
    class Meta:
        model = Problem
        fields = ["id", "idDisplay", "title", "level"]
