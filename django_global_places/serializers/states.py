from rest_framework import serializers

from django_global_places.utils import get_abstract_state_model, use_default_state_model
from django_global_places.app_settings import api_settings as settings
from django_global_places import models


if settings.get_user_setting('INCLUDE_LOCATION') and use_default_state_model():

    if get_abstract_state_model():
        class StateSerializer(serializers.ModelSerializer):
            """Serializer for State model."""

            class Meta:
                model = models.State
                fields = "__all__"

        class StateListSerializer(serializers.ModelSerializer):
            """Serializer for State model."""

            class Meta:
                model = models.State
                fields = ("id", "name", "state_code")


