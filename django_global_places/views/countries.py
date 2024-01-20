from rest_framework import filters as rest_filters

from django.conf import settings

from platform_configurations import models
from platform_configurations.serializers import countries
from django_base.base_utils.base_viewsets import BaseReadOnlyModelViewSet

if settings.INCLUDE_LOCATION:

    class CountryViewSet(BaseReadOnlyModelViewSet):
        """Viewset for Country model."""

        queryset = models.Country.objects.filter(is_active=True)

        serializers = {
            "list": countries.CountryListSerializer,
            "retrieve": countries.CountrySerializer,
        }

        filter_backends =(
            rest_filters.SearchFilter,
            rest_filters.OrderingFilter,
        )

        search_fields = (
            "name",
            "iso3",
        )

        ordering_fields = (
            "id",
            "name",
            "iso3",
        )

        ordering = ("name",)