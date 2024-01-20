from rest_framework.routers import DefaultRouter

from django.conf import settings

from platform_configurations.views import countries, states, cities
from django_base.base_utils.utils import get_abstract_state_model, get_abstract_city_model

router = DefaultRouter()

if settings.INCLUDE_LOCATION:
    router.register("countries", countries.CountryViewSet, basename="countries")
    if get_abstract_state_model():
        router.register("states", states.StateViewSet, basename="states")
        if get_abstract_city_model():
            router.register("cities", cities.CityViewSet, basename="cities")

urlpatterns = []
