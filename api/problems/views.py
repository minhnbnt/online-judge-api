from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from api.models import Problem
from shared.permissions import ReadOnly

from .serializers import ProblemDetailSerializer, ProblemSerializer


class ProblemsList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser | ReadOnly]

    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer


class ProblemUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser | ReadOnly]

    serializer_class = ProblemDetailSerializer
    queryset = Problem.objects.all()
    lookup_field = "id"
