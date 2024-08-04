from rest_framework import serializers

from api.models import Problem


class ProblemDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = ["id", "title", "description", "level"]


class ProblemDetailAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = "__all__"


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = "__all__"

        extra_kwargs = {
            "stdin": {"write_only": True},
            "stdout": {"write_only": True},
            "runFlags": {"write_only": True},
            "timeLimit": {"write_only": True},
            "description": {"write_only": True},
            "memoryLimit": {"write_only": True},
            "compileFlags": {"write_only": True},
        }
