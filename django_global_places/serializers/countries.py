from rest_framework import serializers

from django.conf import settings

from platform_configurations import models


if settings.INCLUDE_LOCATION:
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