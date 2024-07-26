from rest_framework_simplejwt.views import TokenViewBase

from .serializers import TokenObtainPairSerializer as Serializer

serializerModuleName = f"{Serializer.__module__}.{Serializer.__name__}"


class TokenObtainPairView(TokenViewBase):
    _serializer_class = serializerModuleName
