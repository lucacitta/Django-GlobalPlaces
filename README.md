# Django-GlobalPlaces
Plug and play configurations and data for countries, states and cities from all over the globe.

## Requirements
- Django >= 3.8 *
- Python >= 3.8 *
- Django Rest Framework >= 3.13 *
	- This requirement is only necessary if you are using the provided REST endpoints.
- django-filter >= 23.0 *
	- This requirement is only necessary if you are using the provided REST endpoints.
- pytest-django >= 4.0 *
	- This requirement is only necessary if you are running the tests and use Django Rest Framework.
- factory_boy >= 3.0 *
	- This requirement is only necessary if you are running the tests and use Django Rest Framework.

(*) Last tested versions
	- Django==5.1.1
	- Python==3.10.9
	- djangorestframework==3.15.2
	- django-filter==24.3
	- pytest-django==4.9.0
	- factory_boy==3.3.1


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

-  `INCLUDE_LOCATION`: Enables the creation of the models.
-  `LOCATION_SCOPE`: Determines the scope of models required ('country', 'state', or 'city').
-  `INCLUDE_EXPANDED_COUNTRY`: Incorporates additional fields into the Country model.

And you have this 3 optional extra parameters:
-  `COUNTRY_MODEL`: Allows you to integrate the library with a custom country model in case you need extra fields.
-  `STATE_MODEL`: Allows you to integrate the library with a custom state model in case you need extra fields.
-  `CITY_MODEL`: Allows you to integrate the library with a custom city model in case you need extra fields.

Example:
```
GLOBAL_PLACES = {
	"INCLUDE_LOCATION": True,
	"LOCATION_SCOPE": "state",
	"INCLUDE_EXPANDED_COUNTRY": False,
	"COUNTRY_MODEL": "django_global_places.Country",
	"STATE_MODEL": "django_global_places.State",
	"CITY_MODEL": "django_global_places.City",
}
```

Once these variables are configured, your next steps are to run django `migrate` command.

To **populate** the newly created models, you should execute a Django command. This command will create all the necessary objects and update them if they already exist.

```
python manage.py populate_global_places
```

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

### Tests

To run the tests, you need to have the `pytest-django` and `factory_boy` packages installed. You can run the tests with the following command:

```
pytest
```

### Using custom models

The library allows the use of customized models in case additional fields need to be added to the existing models.

It is important that the custom models inherit from the library's abstract classes. For this, there are methods in the utils that return the corresponding abstract model for each one.

Once created, they must be specified in the library configuration as indicated above. This will allow the database population command to use those models instead of the default ones.

### Acknowledgements

Special thanks to the [Countries States Cities Database](https://github.com/dr5hn/countries-states-cities-database) for providing the JSON files used for populating the data.

## Contributing

Create a virtual env, activate it, and then run:

```
python setup.py develop
```

This will install all the required libraries specified in `setup.py`.


### Running django commands

To run any django command without placing the library files in another django project, it is possible to run the following:

```
django-admin <command> --settings=test_settings
```

Where `<command>` can be any of the registered commands, such as `makemigrations`, `migrate`, `populate_global_place`, etc.

#### django-admin troubleshooting

If `django-admin` executable points to a global installation (`which django-admin` points to `/usr/local/bin/django-admin`) and not to the local virtual env one, just replace `django-admin` with the location of the venv executable, ex: `./venv/bin/django-admin`.

### Installing the library in a venv

To install the library in any other virtual env, first activate it, and then run the following command in this projects root (where `setup.py` is located):

```
pip install -e .
```


## Contributors


- [Luca Cittá Giordano](https://www.linkedin.com/in/lucacittagiordano/)

- [Matias Girardi](https://www.linkedin.com/in/matiasgirardi)

- [Juan Ignacio Borrelli](https://www.linkedin.com/in/juan-ignacio-borrelli/)

Maintained and developed by [Linkchar Software Development](https://linkchar.com/).
