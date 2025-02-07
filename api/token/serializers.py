from rest_framework_simplejwt import serializers


class TokenObtainPairSerializer(serializers.TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        return super().get_token(user)