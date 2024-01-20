from rest_framework.routers import DefaultRouter

from django_global_places.app_settings import api_settings as settings
from django_global_places.views import countries, states, cities
from django_global_places.utils import get_abstract_state_model, get_abstract_city_model

router = DefaultRouter()

if settings.get_user_setting('INCLUDE_LOCATION'):
    router.register("global-places/countries", countries.CountryViewSet, basename="countries")
    if get_abstract_state_model():
        router.register("global-places/states", states.StateViewSet, basename="states")
        if get_abstract_city_model():
            router.register("global-places/cities", cities.CityViewSet, basename="cities")