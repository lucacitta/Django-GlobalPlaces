SECRET_KEY = "secret_key_for_testing"


INSTALLED_APPS = (
    "django_global_places",
)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}

GLOBAL_PLACES = {
    "INCLUDE_LOCATION": True,
    "LOCATION_SCOPE": "city",
    "INCLUDE_EXPANDED_COUNTRY": False,
}
