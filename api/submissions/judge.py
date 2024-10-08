from dataclasses import dataclass
from itertools import zip_longest
from typing import Optional

import requests

from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import Response

from api.models import Problem

from .models import Submission
from .serializers import SubmissionViewIdSerializer


def outputsIsSame(collected: str, expected: str) -> bool:
    collectedLines = collected.splitlines()
    expectedLines = expected.splitlines()

    for a, b in zip_longest(collectedLines, expectedLines, fillvalue=""):
        if a.rstrip() != b.rstrip():
            return False

    return True


def getJudgeRequestBody(problem, requestData) -> dict:
    requestBody = {
        "language": requestData["language"],
        "version": requestData["version"],
        "files": [
            {"content": requestData["source"]},
        ],
        "stdin": problem.stdin,
    }

    if problem.runFlags:
        requestBody["args"] = problem.runFlags.splitlines()

    if problem.timeLimit and problem.timeLimit > 0:
        requestBody["run_timeout"] = problem.timeLimit

    if problem.memoryLimit and problem.memoryLimit > 0:
        requestBody["run_memory_limit"] = problem.memoryLimit

    return requestBody


@dataclass
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


def errorResponse(code: str, detail: str, status: int) -> APIException:
    result = APIException(detail, code)
    result.status_code = status

    return result


def handleJudge(request):
    data = request.data

    targetProblem = Problem.objects.get(id=data["problem"])

    requestConfig = {
        "json": getJudgeRequestBody(targetProblem, data),
        "url": f"{settings.JUDGE_URL}/execute",
        "timeout": 60,
    }

    try:
        judgeResponse = requests.post(**requestConfig)
        judgeResponse.raise_for_status()

    except requests.ConnectionError:
        raise errorResponse(
            "service_unavailable",
            "Could not reach the judge server.",
            status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    except requests.Timeout:
        raise errorResponse(
            "gateway_timeout",
            "Judging request timeout.",
            status.HTTP_504_GATEWAY_TIMEOUT,
        )

    except requests.HTTPError as e:
        raise errorResponse(
            "judge_server_error",
            e.response.json(),
            e.response.status_code,
        )

    judgeResult = JudgeResult.fromResponse(
        judgeResponse,
        targetProblem.stdout,
    )

    record = Submission(
        owner=request.user,
        problem=targetProblem,
        language=data["language"],
        version=data["version"],
        source=data["source"],
        judgeResult=judgeResult.overAllResult,
        errorLogs=judgeResult.errorLogs,
    )

    record.save()
    serializer = SubmissionViewIdSerializer(record)

    return Response(serializer.data)
