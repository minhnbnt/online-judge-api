from rest_framework import serializers

from .models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    class Meta:
        model = Submission
        fields = [
            "id",
            "owner",
            "source",
            "problem",
            "language",
            "judgeResult",
            "summittedOn",
        ]

        extra_kwargs = {
            "source": {"write_only": True},
            "judgeResult": {"read_only": True},
        }


class SubmissionDetailSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    class Meta:
        model = Submission
        fields = "__all__"


class SubmissionViewIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ["viewId"]
