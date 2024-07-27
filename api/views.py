from django.conf import settings
from django.http import HttpResponseRedirect

from rest_framework.decorators import api_view
from rest_framework.views import Response


@api_view(["GET"])
def hello(_):
    return Response({"message": "Hello, world!"})


@api_view(["GET"])
def runtimes(_):
    return HttpResponseRedirect(f"{settings.JUDGE_URL}/runtimes")
