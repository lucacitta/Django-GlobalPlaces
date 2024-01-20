from django.conf import settings

from platform_configurations import models
from platform_configurations.serializers import cities
from django_base.base_utils.base_viewsets import BaseReadOnlyModelViewSet


if settings.INCLUDE_LOCATION and models.get_abstract_city_model():
        class CityViewSet(BaseReadOnlyModelViewSet):
            """Viewset for City model."""

            serializers = {
                "list": cities.CitySerializer,
                "retrieve": cities.CitySerializer,
            }


            def get_queryset(self):
                queryset = models.City.objects.filter(
                    is_active=True,
                    state__is_active=True,
                    state__country__is_active=True
                ).select_related('state__country')
                return queryset