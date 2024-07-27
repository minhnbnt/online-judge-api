from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from .models import User
from .serializers import UserRegisterSerializer, UserInfoSerializer

from shared.permissions import IsSelf


class UserInfoView(generics.RetrieveAPIView):
    permission_classes = [IsAdminUser | IsSelf]

    serializer_class = UserInfoSerializer
    queryset = User.objects.all()
    lookup_field = "id"


class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
