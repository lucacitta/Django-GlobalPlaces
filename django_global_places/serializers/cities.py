from rest_framework import serializers

from django_global_places.app_settings import api_settings as settings
from django_global_places.utils import get_abstract_city_model
from django_global_places import models


if settings.get_user_setting('INCLUDE_LOCATION'):

    if get_abstract_city_model():
        class CitySerializer(serializers.ModelSerializer):
            """Serializer for City model."""

            class Meta:
                model = models.City
                fields = "__all__"

        class CityListSerializer(serializers.ModelSerializer):
            """Serializer for City model."""

            class Meta:
                model = models.City
                fields = ("id", "name",)