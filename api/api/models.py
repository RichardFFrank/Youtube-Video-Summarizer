from django.core.exceptions import ValidationError
from django.db import models
from urllib.parse import urlparse
from rest_framework import serializers


def validate_youtube_url(value):
    youtube_domains = ["www.youtube.com", "youtube.com", "m.youtube.com"]
    parsed_url = urlparse(value)
    if parsed_url.netloc not in youtube_domains:
        raise ValidationError("The URL must be a YouTube URL (e.g., www.youtube.com).")


class YouTubeModel(models.Model):
    yt_url = models.URLField(validators=[validate_youtube_url])

    def __str__(self):
        return self.yt_url


class YouTubeModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = YouTubeModel
        fields = ["yt_url"]
