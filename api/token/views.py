from rest_framework_simplejwt.views import TokenViewBase

from .serializers import TokenObtainPairSerializer


class TokenObtainPairView(TokenViewBase):
    _serializer_class = TokenObtainPairSerializer
