from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import status

from .models import Problem
from .serializers import ProblemDetailSerializer, ProblemSerializer


@api_view(["GET"])
def hello(request):
    return Response({"message": "Hello, world!"})


@api_view(["GET"])
def getProblems(request):
    problems = Problem.objects.all()
    serializer = ProblemSerializer(problems, many=True)

    return Response(serializer.data)


@api_view(["GET"])
def getProblemDetail(request, idDisplay: str):
    try:
        target = Problem.objects.get(idDisplay=idDisplay)
        serializer = ProblemDetailSerializer(target)

        return Response(serializer.data)

    except Problem.DoesNotExist:
        return Response(
            {"error": f"problem with id '{idDisplay}' not found!"},
            status.HTTP_404_NOT_FOUND,
        )
