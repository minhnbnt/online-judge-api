from rest_framework import serializers

from shared import fields
from api.problems.serializers import ProblemSerializer

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
    problem = ProblemSerializer(many=False)
    owner = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )

    viewId = fields.ShortUUIDField()

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


class SubmissionViewIdSerializer(serializers.Serializer):
    viewId = fields.ShortUUIDField()
