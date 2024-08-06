from django.core.exceptions import ObjectDoesNotExist

from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from shared.permissions import IsOwner, ReadOnly
from shared.shortuuid import uuidShortener

from .judge import handleJudge
from .models import Submission
from .serializers import (
    SubmissionDetailSerializer,
    SubmissionSerializer,
    SubmissionViewIdSerializer,
)


class SubmissionView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    queryset = Submission.objects.all()

    filter_backends = [OrderingFilter, DjangoFilterBackend]
    filterset_fields = ["problem", "owner"]
    ordering = ["-id"]

    def get_serializer_class(self):
        if self.request.method == "GET":
            return SubmissionSerializer

        return SubmissionDetailSerializer

    def create(self, request):
        Serializer = self.get_serializer_class()
        serializer = Serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        return handleJudge(request)


class SubmissionViewId(generics.RetrieveAPIView):
    permission_classes = [IsOwner | IsAdminUser]

    serializer_class = SubmissionViewIdSerializer
    queryset = Submission.objects.all()
    lookup_field = "id"


class SubmissionDetailView(generics.RetrieveAPIView):
    serializer_class = SubmissionDetailSerializer
    queryset = Submission.objects.all()

    def get_object(self):
        querySet = self.get_queryset()
        shorteduuid = self.kwargs["viewId"]

        try:
            uuid = uuidShortener.decode(shorteduuid)
            obj = querySet.get(viewId=uuid)

            return obj

        # ValueError will only raise when input
        # length very long, so no uuid will match this
        except (ObjectDoesNotExist, ValueError):
            raise NotFound()
