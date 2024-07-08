from rest_framework import serializers

from api.models import Problem


class ProblemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = "__all__"


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = "__all__"
        extra_kwargs = {"description": {"write_only": True}}
