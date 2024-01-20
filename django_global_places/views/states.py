from django_filters import rest_framework as filters

from rest_framework import filters as rest_filters

from django.conf import settings

from platform_configurations import models
from platform_configurations.serializers import states
from django_base.base_utils.base_viewsets import BaseReadOnlyModelViewSet



if settings.INCLUDE_LOCATION and models.get_abstract_state_model():
        class StateViewSet(BaseReadOnlyModelViewSet):
            """Viewset for State model."""

            serializers = {
                "list": states.StateListSerializer,
                "retrieve": states.StateSerializer,
            }

            filter_backends = (
                filters.DjangoFilterBackend,
                rest_filters.SearchFilter,
                rest_filters.OrderingFilter,
            )

            filterset_fields = (
                "country",
            )

            search_fields = (
                "name",
                "state_code",
            )

            ordering_fields = (
                "id",
                "name",
                "state_code",
            )

            ordering = ("name",)

            def get_queryset(self):
                queryset = models.State.objects.filter(
                    is_active=True,
                    country__is_active=True
                ).select_related('country')
                return queryset
