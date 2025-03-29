from dataclasses import dataclass
from itertools import zip_longest
from typing import Optional

import requests
from django.conf import settings
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.views import Response

from api.models import Problem
from api.users.models import User
from .models import Submission
from .serializers import SubmissionViewIdSerializer


def outputs_are_same(collected: str, expected: str) -> bool:
    collected_lines = collected.splitlines()
    expected_lines = expected.splitlines()

    for a, b in zip_longest(collected_lines, expected_lines, fillvalue=""):
        if a.rstrip() != b.rstrip():
            return False

    return True


def get_judge_request_body(problem: Problem, request_data: dict) -> dict:
    request_body = {
        "language": request_data["language"],
        "version": request_data["version"],
        "files": [
            {"content": request_data["source"]},
        ],
        "stdin": problem.stdin,
    }

    if problem.runFlags:
        request_body["args"] = problem.runFlags.splitlines()

    if problem.timeLimit and problem.timeLimit > 0:
        request_body["run_timeout"] = problem.timeLimit

    if problem.memoryLimit and problem.memoryLimit > 0:
        request_body["run_memory_limit"] = problem.memoryLimit

    return request_body


@dataclass
class JudgeResult:
    overall_result: str
    errorLogs: Optional[str]

    @classmethod
    def from_response(cls, judge_response, expected_output: str):
        judge_response = judge_response.json()

        try:
            compile_log = judge_response["compile"]
            if compile_log["code"] != 0:
                return cls("CE", compile_log["stderr"])

        except KeyError:
            pass

        run_log = judge_response["run"]
        if run_log["signal"] == "SIGKILL":
            return cls("TLE", None)

        if run_log["code"] != 0:
            over_all_result = "IR"
            error_logs = run_log["stderr"]

            if not error_logs:
                over_all_result = "RTE"
                error_logs = None

            return cls(over_all_result, error_logs)

        if outputs_are_same(run_log["stdout"], expected_output):
            return cls("AC", None)
        else:
            return cls("WA", None)


def get_error_response(code: str, detail: str, status_code: int) -> APIException:
    result = APIException(detail, code)
    result.status_code = status_code

    return result


def handle_judge(user: User, request_body: dict):
    targetProblem = Problem.objects.get(id=request_body["problem"])  # noqa

    request_config = {
        "json": get_judge_request_body(targetProblem, request_body),
        "url": f"{settings.JUDGE_URL}/execute",
        "timeout": 60,
    }

    try:
        judge_response = requests.post(**request_config)
        judge_response.raise_for_status()

    except requests.ConnectionError:
        raise get_error_response(
            "service_unavailable",
            "Could not reach the judge server.",
            status.HTTP_503_SERVICE_UNAVAILABLE,
        )

    except requests.Timeout:
        raise get_error_response(
            "gateway_timeout",
            "Judging request timeout.",
            status.HTTP_504_GATEWAY_TIMEOUT,
        )

    except requests.HTTPError as e:
        raise get_error_response(
            "judge_server_error",
            e.response.json(),
            e.response.status_code,
        )

    judge_result = JudgeResult.from_response(
        judge_response,
        targetProblem.stdout,
    )

    record = Submission(
        owner=user,
        problem=targetProblem,
        source=request_body["source"],
        version=request_body["version"],
        language=request_body["language"],
        errorLogs=judge_result.errorLogs,
        judgeResult=judge_result.overall_result,
    )

    record.save()
    serializer = SubmissionViewIdSerializer(record)

    return Response(serializer.data)
