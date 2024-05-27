from django_filters import rest_framework as filters

from rest_framework import filters as rest_filters

from django_global_places.viewsets_utils import BaseReadOnlyModelViewSet
from django_global_places.app_settings import api_settings as settings
from django_global_places.utils import get_abstract_state_model
from django_global_places.serializers import states
from django_global_places import models



if settings.get_user_setting('INCLUDE_LOCATION') and get_abstract_state_model():
        class StateViewSet(BaseReadOnlyModelViewSet):
            """Viewset for State model."""

            queryset = models.State.objects.filter(
                    is_active=True,
                    country__is_active=True
                ).select_related('country')

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
