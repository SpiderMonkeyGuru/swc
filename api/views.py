from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets

from api.models import ShortenedURL
from api.serializers import URLShortenerSerializer


class URLShortenerViewSet(
    viewsets.ModelViewSet,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
):
    queryset = ShortenedURL.objects.all()
    serializer_class = URLShortenerSerializer


def expand_url(request, short_code: str) -> HttpResponseRedirect:
    url_mapping = get_object_or_404(ShortenedURL, short_code=short_code)
    return HttpResponseRedirect(url_mapping.original_url)
