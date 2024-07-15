from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from api.permissions import ReadOnly

from .judge import handleJudge
from .serializers import SubmissionSerializer


class SubmissionView(generics.CreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated | ReadOnly]

    serializer_class = SubmissionSerializer

    def create(self, request):
        SerializerClass = self.get_serializer_class()
        return handleJudge(SerializerClass, request)
