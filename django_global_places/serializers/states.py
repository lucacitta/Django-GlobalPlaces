from rest_framework import serializers

from django.conf import settings

from platform_configurations import models


if settings.INCLUDE_LOCATION:

    if models.get_abstract_state_model():
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


