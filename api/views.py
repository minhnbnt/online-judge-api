from django.conf import settings
from django.http import HttpResponseRedirect

from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.views import Response


@api_view(["GET"])
def hello(request: Request):
    message = "Hello, world!"

    if username := request.user.username:
        message = f"Hello, your username is {username}."

    return Response({"message": message})


@api_view(["GET"])
def runtimes(_):
    return HttpResponseRedirect(f"{settings.JUDGE_URL}/runtimes")
