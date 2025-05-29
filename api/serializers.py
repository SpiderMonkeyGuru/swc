from rest_framework.serializers import ModelSerializer

from .models import ShortenedURL


class URLShortenerSerializer(ModelSerializer):
    class Meta:
        model = ShortenedURL
        fields = (
            "original_url",
            "shortened_url",
        )
        extra_kwargs = {
            "original_url": {"write_only": True},
        }


class URLExpanderSerializer(ModelSerializer):
    class Meta:
        model = ShortenedURL
        fields = ("original_url",)
