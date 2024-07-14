from rest_framework import serializers


class SubmissionSerializer(serializers.Serializer):
    problemId = serializers.CharField(required=True)

    language = serializers.CharField(required=True)
    version = serializers.CharField(required=True)
    source = serializers.CharField(
        required=True,
        style={"base_template": "textarea.html"},
    )
