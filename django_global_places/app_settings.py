from django.conf import settings

USER_SETTINGS = getattr(settings, "GLOBAL_PLACES", None)

DEFAULTS = {
    'INCLUDE_LOCATION': True,
    'LOCATION_SCOPE': 'country', 
    'INCLUDE_EXPANDED_COUNTRY': True,
    'COUNTRY_MODEL': 'django_global_places.Country',
    'STATE_MODEL': 'django_global_places.State',
    'CITY_MODEL': 'django_global_places.City',
}

class APISettings:
    def __init__(self, user_settings=None, defaults=None):
        self.defaults = defaults
        self._user_settings = self.__check_user_settings(user_settings) \
            if user_settings else {}

    def __check_user_settings(self, user_settings):
        for setting in user_settings:
            if setting not in self.defaults:
                raise RuntimeError(f"The {setting} setting is not a valid setting for django_global_places.")

            if setting == 'LOCATION_SCOPE' and user_settings[setting] not in ['country', 'state', 'city']:
                raise RuntimeError(f"The {setting} setting must be one of ['country', 'state', 'city'].")

        models = ['COUNTRY_MODEL', 'STATE_MODEL', 'CITY_MODEL']
        for model in models:
            if model not in user_settings:
                user_settings[model] = self.defaults[model]

        return user_settings

    def get_user_setting(self, attr):
        try:
            return self._user_settings[attr]
        except KeyError:
            return self.defaults[attr]


api_settings = APISettings(USER_SETTINGS, DEFAULTS)