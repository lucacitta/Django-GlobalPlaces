from django_global_places.abstract_models import AbstractState, AbstractCity
from django_global_places.utils import (
    get_abstract_country_model,
    use_default_country_model,
    use_default_state_model,
    use_default_city_model
)
from django_global_places.app_settings import api_settings as settings

if use_default_country_model():
    class Country(get_abstract_country_model()):
        class Meta:
            verbose_name_plural = "Countries"

if use_default_state_model():
    class State(AbstractState):
        class Meta:
            verbose_name_plural = "States"

if use_default_city_model():
    class City(AbstractCity):
        class Meta:
            verbose_name_plural = "Cities"