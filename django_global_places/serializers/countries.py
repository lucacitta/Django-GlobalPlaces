from rest_framework import serializers

from django_global_places.app_settings import api_settings as settings
from django_global_places import models


if settings.get_user_setting('INCLUDE_LOCATION'):
    class CountrySerializer(serializers.ModelSerializer):
        """Serializer for Country model."""

        class Meta:
            model = models.Country
            fields = "__all__"

    class CountryListSerializer(serializers.ModelSerializer):
        """Serializer for Country model."""

        class Meta:
            model = models.Country
            fields = ("id", "name", "iso3")