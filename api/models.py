import uuid

from django.conf import settings
from django.db import models
from django.db.models import Value
from django.db.models.functions import Concat


def create_short_code():
    return str(uuid.uuid4()).replace("-", "")[:10]


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ShortenedURL(TimestampedModel):
    original_url = models.URLField(max_length=2000)
    short_code = models.CharField(
        max_length=10,
        unique=True,
        db_index=True,
        default=create_short_code,
    )
    shortened_url = models.GeneratedField(
        expression=Concat(Value(settings.SERVER_ORIGIN), "short_code"),
        output_field=models.URLField(),
        db_persist=True,
    )
