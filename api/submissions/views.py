import shortuuid
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.permissions import IsOwner, ReadOnly

from .judge import handleJudge
from .models import Submission
from .serializers import (SubmissionDetailSerializer, SubmissionSerializer,
                          SubmissionViewIdSerializer)


class SubmissionView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated | ReadOnly]

    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["problem", "owner"]

    def create(self, request):
        SerializerClass = self.get_serializer_class()
        serializer = SerializerClass(data=request.data)

        if serializer.is_valid():
            return handleJudge(request)

        return Response(
            serializer.errors,
            status.HTTP_400_BAD_REQUEST,
        )


class SubmissionViewId(generics.RetrieveAPIView):
    permission_classes = [IsOwner]

    serializer_class = SubmissionViewIdSerializer
    queryset = Submission.objects.all()
    lookup_field = "id"


class SubmissionDetailView(generics.RetrieveAPIView):
    serializer_class = SubmissionDetailSerializer
    queryset = Submission.objects.all()
    lookup_field = "viewId"

    def get_object(self):
        querySet = self.get_queryset()
        shorteduuid = self.kwargs["viewId"]

        uuid = shortuuid.decode(shorteduuid)
        obj = get_object_or_404(querySet, viewId=uuid)

        return obj
