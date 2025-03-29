from django.template.defaulttags import comment
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from api.problems.models import Problem, Comment
from shared.permissions import ReadOnly
from .serializers import (
    CommentSerializer,
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


class CommentListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    serializer_class = CommentSerializer
    lookup_field = "id"

    ordering = ["submittedOn"]

    def get_queryset(self):
        problem_id = self.kwargs["id"]
        return Comment.objects.filter(problem_id=problem_id)

    def perform_create(self, serializer):
        new_comment = Comment(
            user=self.request.user,
            problem_id=self.kwargs["id"],
            **self.request.data
        )

        return new_comment.save()