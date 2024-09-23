from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser

from api.models import Problem
from shared.permissions import ReadOnly
from .serializers import (
    ProblemDetailAdminSerializer,
    ProblemDetailSerializer,
    ProblemSerializer,
)


class ProblemsListView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser | ReadOnly]

    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer

    filter_backends = [OrderingFilter, SearchFilter]
    search_fields = ["id", "title"]
    ordering = ["id"]


class ProblemDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser | ReadOnly]

    queryset = Problem.objects.all()
    lookup_field = "id"

    def get_serializer_class(self):
        if not self.request.user.is_staff:
            return ProblemDetailSerializer

        return ProblemDetailAdminSerializer
