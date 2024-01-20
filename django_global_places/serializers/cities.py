from rest_framework import serializers

from django.conf import settings

from platform_configurations import models


if settings.INCLUDE_LOCATION:

    if models.get_abstract_city_model():
        class CitySerializer(serializers.ModelSerializer):
            """Serializer for City model."""

            class Meta:
                model = models.City
                fields = "__all__"

        class CityListSerializer(serializers.ModelSerializer):
            """Serializer for City model."""

            class Meta:
                model = models.City
                fields = ("id", "name", "code")