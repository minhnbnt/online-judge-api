import shortuuid

from django.core.exceptions import ObjectDoesNotExist
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from shared.permissions import IsOwner, ReadOnly

from .judge import handleJudge
from .models import Submission
from .serializers import (
    SubmissionDetailSerializer,
    SubmissionSerializer,
    SubmissionViewIdSerializer,
)


class SubmissionView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    queryset = Submission.objects.all()  # noqa

    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["problem", "owner"] # noqa
    ordering = ["-id"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return SubmissionSerializer

        return SubmissionDetailSerializer

    def create(self, request, **kwargs):
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        return handleJudge(request)


class SubmissionViewId(generics.RetrieveAPIView):
    permission_classes = [IsOwner | IsAdminUser]

    serializer_class = SubmissionViewIdSerializer
    queryset = Submission.objects.all()  # noqa
    lookup_field = "id"


class SubmissionDetailView(generics.RetrieveAPIView):
    serializer_class = SubmissionDetailSerializer
    queryset = Submission.objects.all()  # noqa

    def get_object(self):
        query_set = self.get_queryset()
        shorted_uuid = self.kwargs["viewId"]

        try:
            uuid = shortuuid.decode(shorted_uuid)
            obj = query_set.get(viewId=uuid)

            return obj

        # ValueError will only raise when input
        # length very long, so no uuid will match this
        except (ObjectDoesNotExist, ValueError):
            raise NotFound()
