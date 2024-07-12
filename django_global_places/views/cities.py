from django_filters import rest_framework as filters

from rest_framework import filters as rest_filters

from django_global_places import models
from django_global_places.serializers import cities
from django_global_places.app_settings import api_settings as settings
from django_global_places.viewsets_utils import BaseReadOnlyModelViewSet
from django_global_places.utils import use_default_city_model

if settings.get_user_setting('INCLUDE_LOCATION') and use_default_city_model():
        class CityViewSet(BaseReadOnlyModelViewSet):
            """Viewset for City model."""

            queryset = models.City.objects.filter(
                    is_active=True,
                    state__is_active=True,
                    state__country__is_active=True
                ).select_related('state', 'state__country')

            serializers = {
                "list": cities.CityListSerializer,
                "retrieve": cities.CitySerializer,
            }

            filter_backends = (
                filters.DjangoFilterBackend,
                rest_filters.SearchFilter,
                rest_filters.OrderingFilter,
            )

            filterset_fields = (
                "state",
                "state__country",
            )

            search_fields = (
                "name",
            )

            ordering_fields = (
                "id",
                "name",
            )

            ordering = ("name",)