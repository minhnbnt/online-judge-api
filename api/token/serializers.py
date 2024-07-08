from rest_framework_simplejwt import serializers


class TokenObtainPairSerializer(serializers.TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        return token
