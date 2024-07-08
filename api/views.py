from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import status
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Problem
from .serializers import (ProblemDetailSerializer, ProblemSerializer,
                          UserSerializer)
from .utils import ReadOnly


@api_view(["GET"])
def hello(_):
    return Response({"message": "Hello, world!"})


class ProblemsList(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [(IsAdminUser & IsAuthenticated) | ReadOnly]

    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer


class ProblemUpdate(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [(IsAdminUser & IsAuthenticated) | ReadOnly]

    serializer_class = ProblemDetailSerializer
    queryset = Problem.objects.all()
    lookup_field = "id"


class UserRegister(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"user": serializer.data}, status.HTTP_201_CREATED)
