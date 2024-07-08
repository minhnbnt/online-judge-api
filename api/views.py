from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.views import Response

from .serializers import UserSerializer


@api_view(["GET"])
def hello(request):
    return Response({"message": "Hello, world!"})


class UserRegister(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"user": serializer.data}, status.HTTP_201_CREATED)
