from django_global_places.abstract_models import AbstractState, AbstractCity
from django_global_places.utils import (
    get_abstract_country_model,
)

class Country(get_abstract_country_model()):
    class Meta:
        verbose_name_plural = "Countries"

class State(AbstractState):
    class Meta:
        verbose_name_plural = "States"

class City(AbstractCity):
    class Meta:
        verbose_name_plural = "Cities"