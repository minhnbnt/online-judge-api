from rest_framework import serializers

from shared import fields
from api.problems.serializers import ProblemSerializer

from .models import Submission


class SubmissionSerializer(serializers.ModelSerializer):
    problem = ProblemSerializer(many=False)
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


class SubmissionDetailSerializer(serializers.ModelSerializer):
    owner = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    viewId = fields.ShortUUIDField(read_only=True)

    class Meta:
        model = Submission
        fields = [
            "id",
            "viewId",
            "owner",
            "source",
            "problem",
            "language",
            "version",
            "judgeResult",
            "summittedOn",
        ]

        extra_kwargs = {
            "judgeResult": {"read_only": True},
            "submittedOn": {"read_only": True},
        }


class SubmissionViewIdSerializer(serializers.Serializer):
    viewId = fields.ShortUUIDField()
