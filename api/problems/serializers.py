from rest_framework import serializers

from .models import Problem, Comment


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


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = ["user", "comment", "commentedOn"]

        extra_kwargs = {
            "user": {"read_only": True},
            "commentedOn": {"read_only": True}
        }
