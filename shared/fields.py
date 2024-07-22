from uuid import UUID

import shortuuid

from rest_framework import serializers


class ShortUUIDField(serializers.UUIDField):
    def to_internal_value(self, data):
        data = shortuuid.decode(data)
        return super().to_internal_value(data)

    def to_representation(self, value):
        value = super().to_representation(value)
        return shortuuid.encode(UUID(value))
