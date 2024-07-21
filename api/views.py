from django.conf import settings
from django.http import HttpResponseRedirect
from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.views import Response

from .serializers import UserSerializer


@api_view(["GET"])
def hello(request):
    return Response({"message": "Hello, world!"})


@api_view(["GET"])
def runtimes(request):
    return HttpResponseRedirect(f"{settings.JUDGE_URL}/runtimes")


class UserRegister(generics.CreateAPIView):
    serializer_class = UserSerializer
