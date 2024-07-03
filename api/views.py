from ninja import NinjaAPI
from ninja.errors import HttpError

from .models import Problem
from .schemas import ProblemDescSchema, ProblemSchema

api = NinjaAPI()


@api.get("hello/")
def hello(request):
    return {"message": "Hello, world!"}


@api.get("problems/", response=list[ProblemSchema])
def getProblems(request):
    return Problem.objects.all()


@api.get("problems/description/{idDisplay}", response=ProblemDescSchema)
def getProblemDescription(request, idDisplay: str):
    try:
        return Problem.objects.get(idDisplay=idDisplay)
    except Problem.DoesNotExist:
        raise HttpError(404, f"Problem with id {idDisplay} not found")
