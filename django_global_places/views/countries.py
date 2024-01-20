from rest_framework import filters as rest_filters

from django_global_places import models
from django_global_places.serializers import countries
from django_global_places.app_settings import api_settings as settings
from django_global_places.viewsets_utils import BaseReadOnlyModelViewSet

if settings.get_user_setting('INCLUDE_LOCATION'):

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