
# Django-GlobalPlaces
Plug and play configurations and data for countries, states and cities from all over the globe.

## Requirements
- Django >= 3.8 *
- Python >= 3.8 *
- Django Rest Framework >=  3.13 *
	- This requirement is only necessary if you are using the provided REST endpoints.
- django-filter >= 23.0 *
	- This requirement is only necessary if you are using the provided REST endpoints.


(*) Not tested with earlier versions.

## Quick Setup

Install package

    pip install django-global-places
    
Add `django_global_places` app to INSTALLED_APPS in your django settings.py:

```python
INSTALLED_APPS = (
    ...,
    "django.contrib.staticfiles",
    'django_global_places'
    'rest_framework', # required only if using the provided REST endpoints
     ...,
)
```
    
(Optional) Include viewset routes

```python
from django_global_places.urls import router as django_global_places_router
your_router.registry.extend(django_global_places_router.registry)
```
    

### Explanation


This library handles the configuration and creation of `Countries`, `States`, and `Cities`.

After installation, you need to specify three parameters in your `settings.py` file:

-   `INCLUDE_LOCATION`: Enables the creation of the models.
-   `LOCATION_SCOPE`: Determines the scope of models required ('countries', 'states', or 'cities').
-   `INCLUDE_EXPANDED_COUNTRY`: Incorporates additional fields into the Country model.

Example:

    GLOBAL_PLACES = {
	    "INCLUDE_LOCATION": True,
	    "LOCATION_SCOPE": "state",
	    "INCLUDE_EXPANDED_COUNTRY": False,
    }


Once these variables are configured, your next steps are to run `makemigrations` and `migrate`.

To **populate** the newly created models, you should execute a Django command. This command will create all the necessary objects and update them if they already exist.

    python manage.py populate_global_places

### Rest endpoints

Three viewsets are included, one for each model: `Country`, `State`, and `City`. Each viewset features:

A list view displaying a summary of the objects.
A detail view presenting comprehensive information about each object.

- CountryViewSet:
	- url: global-places/countries
	- search fields: `name` and `iso3`
	- ordering fields: `id`, `name` and `iso3`

- StateViewSet:
	- url: global-places/states
	- search fields: `name` and `state_code`
	- ordering fields: `id`, `name` and `state_code`
	- filtering fields: `country`

- CityViewSet:
	- url: global-places/cities
	- search fields: `name`
	- ordering fields: `id` and `name`
	- filtering fields: `state`, `state__country`

Full examples [here](https://www.postman.com/restless-zodiac-765340/workspace/django-globalplaces/collection/18007906-46245b57-0675-4bfb-ae41-c71ee6f6f6f5?action=share&creator=18007906) in Postman collection.

### Acknowledgements

Special thanks to the [Countries States Cities Database](https://github.com/dr5hn/countries-states-cities-database) for providing the JSON files used for populating the data.

## Contributing

-   [Luca Cittá Giordano](https://www.linkedin.com/in/lucacittagiordano/)
    
-   [Matias Girardi](https://www.linkedin.com/in/matiasgirardi)

Maintained and developed by [Linkchar Software Development](https://linkchar.com/).


