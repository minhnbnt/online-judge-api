from itertools import zip_longest
from typing import Optional

from django.conf import settings
from rest_framework import generics, status
from rest_framework.compat import requests
from rest_framework.decorators import api_view
from rest_framework.views import Response

from api.judge.models import Submission

from .serializers import SubmissionSerializer


def outputsIsSame(collected: str, expected: str) -> bool:
    collectedLines = collected.splitlines()
    expectedLines = expected.splitlines()

    for a, b in zip_longest(collectedLines, expectedLines, fillvalue=""):
        if a.rstrip() != b.rstrip():
            return False

    return True


class JudgeResult:
    overAllResult: str
    errorLogs: Optional[str]

    @classmethod
    def fromResponse(cls, judgeResponse, expectedOutput):
        judgeResponse = judgeResponse.json()

        try:
            compileLog = judgeResponse["compile"]
            if compileLog["code"] != 0:
                return cls("CE", compileLog["stderr"])

        except KeyError:
            pass

        runLog = judgeResponse["run"]
        if runLog["signal"] == "SIGKILL":
            return cls("TLE", None)

        if runLog["code"] != 0:
            overAllResult = "IR"
            errorLogs = runLog["stderr"]

            if not errorLogs:
                overAllResult = "RTE"
                errorLogs = None

            return cls(overAllResult, errorLogs)

        if outputsIsSame(runLog["stdout"], expectedOutput):
            return cls("AC", None)

        return cls("WA", None)

    def __init__(self, overAllResult, errorLogs):
        self.overAllResult = overAllResult
        self.errorLogs = errorLogs


@api_view(["GET"])
def hello(request):
    return Response({"message": "Hello, world!"})


class SubmissionViews(generics.CreateAPIView):
    serializer_class = SubmissionSerializer

    def create(self, request):
        data = request.data

        SerializerClass = self.get_serializer_class()
        serializer = SerializerClass(data=data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status.HTTP_400_BAD_REQUEST,
            )

        # TODO: get problems judge rules from database

        requestBody = {
            "language": data["language"],
            "version": data["version"],
            "files": [
                {"content": data["source"]},
            ],
        }

        judgeResponse = requests.post(settings.JUDGE_URL, json=requestBody)
        # TODO: handle on no internet connection
        if judgeResponse.status_code != status.HTTP_200_OK:
            return Response(
                judgeResponse.json(),
                judgeResponse.status_code,
            )

        judgeResult = JudgeResult.fromResponse(judgeResponse, "Hello, world!")

        record = Submission(
            problemId=data["problemId"],
            language=data["language"],
            version=data["version"],
            source=data["source"],
            judgeResult=judgeResult.overAllResult,
            errorLog=judgeResult.errorLogs,
        )

        record.save()

        return Response(vars(judgeResult))
