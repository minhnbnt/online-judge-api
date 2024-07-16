from rest_framework import serializers

from .models import Submission


class SubmissionSerializer(serializers.Serializer):
    problem_id = serializers.CharField(required=True)

    language = serializers.CharField(required=True)
    version = serializers.CharField(required=True)
    source = serializers.CharField(
        required=True,
        write_only=True,
        style={"base_template": "textarea.html"},
    )


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
