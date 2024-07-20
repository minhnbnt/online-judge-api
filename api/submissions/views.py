from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.permissions import IsOwner, ReadOnly

from .judge import handleJudge
from .models import Submission
from .serializers import (SubmissionDetailSerializer, SubmissionSerializer,
                          SubmissionViewIdSerializer)


class SubmissionView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated | ReadOnly]

    serializer_class = SubmissionSerializer
    queryset = Submission.objects.all()

    def create(self, request):
        SerializerClass = self.get_serializer_class()
        serializer = SerializerClass(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status.HTTP_400_BAD_REQUEST,
            )

        return handleJudge(request)


class SubmissionViewId(generics.RetrieveAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwner]

    serializer_class = SubmissionViewIdSerializer
    queryset = Submission.objects.all()
    lookup_field = "id"


class SubmissionDetailView(generics.RetrieveAPIView):
    serializer_class = SubmissionDetailSerializer
    queryset = Submission.objects.all()
    lookup_field = "viewId"
