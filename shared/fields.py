from uuid import UUID

from rest_framework import serializers

from .shortuuid import uuidShortener


class ShortUUIDField(serializers.UUIDField):
    def to_internal_value(self, data):
        data = uuidShortener.decode(data)
        return super().to_internal_value(data)

    def to_representation(self, value):
        value = super().to_representation(value)
        return uuidShortener.encode(UUID(value))
