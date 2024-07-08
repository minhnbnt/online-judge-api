from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.models import Problem

from .permissions import ReadOnly
from .serializers import ProblemDetailSerializer, ProblemSerializer


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
