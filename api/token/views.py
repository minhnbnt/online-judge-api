from rest_framework_simplejwt.views import TokenViewBase


class TokenObtainPairView(TokenViewBase):
    _serializer_class = "api.token.serializers.TokenObtainPairSerializer"
