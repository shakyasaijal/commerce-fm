from rest_framework import serializers


class ResendSerializer(serializers.Serializer):
    """`
    Serializer for password reset endpoint.
    """
    email = serializers.EmailField(required=True)