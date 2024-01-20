from django.conf import settings

from django_base.base_utils.utils import (
    get_abstract_country_model,
    get_abstract_state_model,
    get_abstract_city_model
)


if settings.INCLUDE_LOCATION:
    class Country(get_abstract_country_model()):
        class Meta:
            verbose_name_plural = "Countries"
    
    if abstract_state_model := get_abstract_state_model():
        class State(abstract_state_model):
            class Meta:
                verbose_name_plural = "States"


    if abstract_city_model := get_abstract_city_model():
        class City(abstract_city_model):
            class Meta:
                verbose_name_plural = "Cities"