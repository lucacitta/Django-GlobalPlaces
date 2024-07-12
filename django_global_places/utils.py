from django_global_places.app_settings import api_settings as settings
from django_global_places import abstract_models

def get_abstract_country_model():
    return abstract_models.AbstactExpandedCountry \
        if settings.get_user_setting('INCLUDE_EXPANDED_COUNTRY') \
        else abstract_models.AbstactCountry

def get_abstract_state_model():
    return abstract_models.AbstractState \
        if not settings.get_user_setting('LOCATION_SCOPE') == 'country' \
        else None

def get_abstract_city_model():
    return abstract_models.AbstractCity \
        if settings.get_user_setting('LOCATION_SCOPE') == 'city' \
        else None

def use_default_country_model():
    return settings.get_user_setting('COUNTRY_MODEL') == 'django_global_places.Country'

def use_default_state_model():
    return settings.get_user_setting('STATE_MODEL') == 'django_global_places.State'

def use_default_city_model():
    return settings.get_user_setting('CITY_MODEL') == 'django_global_places.City'

