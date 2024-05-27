import pandas as pd

import json

import time

from io import StringIO

import requests

from django.core.management.base import BaseCommand

from django_global_places.app_settings import api_settings as settings
from django_global_places import models 


class Command(BaseCommand):
    """Django command to populate location models."""

    data_uls = {
        'country':f'/countries.json',
        'state':f'/countries+states.json',
        'city':f'/countries+states+cities.json'
    }

    model_creator = {
        'country': '_create_country_object',    
        'state': '_create_state_object',
        'city': '_create_city_object'
    }

    related = {
        'country': [],
        'state': ['states'],
        'city': ['states', 'states__cities']
    }

    base_country_fields = [
        'name',
        'iso3',
        'latitude',
        'longitude',
    ]

    extended_country_fields = base_country_fields + [
        'iso2',
        'numeric_code',
        'phone_code',
        'currency',
        'currency_name',
        'currency_symbol'
    ]

    approved_state_types = [
        'state','province', 'metropolitan region', 'Region', 'region', None,
        'territory','canton','department','federal district','capital city',
        'autonomous region', 'autonomous community','autonomous region','republic'
        ]

    extra_pos = 1 \
        if settings.get_user_setting('LOCATION_SCOPE') == 'city' \
        else 0

    country_extra_pos = (1 \
                        if settings.get_user_setting('LOCATION_SCOPE') == 'country' \
                        else 0) + extra_pos

    def _get_base_data_urls(self):
        self.base_data_url = 'https://raw.githubusercontent.com/dr5hn/countries-states-cities-database/master/'
        self.buenos_aires_data_url = 'https://apis.datos.gob.ar/georef/api/municipios?provincia=06&max=999'

    def _get_data_url(self):
        if not settings.get_user_setting('INCLUDE_LOCATION'):
            raise Exception('The "INCLUDE_LOCATION" setting must be True to populate location models')
        return self.base_data_url + self.data_uls[settings.get_user_setting('LOCATION_SCOPE')]

    def _get_data(self):
        response = requests.get(self._get_data_url())
        if response.status_code != 200:
            raise Exception('Error getting data from url')
        data = pd.read_json(StringIO(response.text))
        return data

    def _get_all_countries(self):
        return models.Country.objects.prefetch_related(
                *self.related['country']
            ).all()

    def _update_country(self, item, all_countries, counties_to_update):
        country = all_countries.get(name=item[0 + self.country_extra_pos])
        country.iso3=item[1 + self.country_extra_pos]
        country.latitude=item[18 + self.country_extra_pos]
        country.longitude=item[19 + self.country_extra_pos]
        country.iso2 = item[2 + self.country_extra_pos]
        country.numeric_code = item[3 + self.country_extra_pos]
        country.phone_code = item[4 + self.country_extra_pos]
        country.currency = item[7 + self.country_extra_pos]
        country.currency_name = item[8 + self.country_extra_pos]
        country.currency_symbol = item[9 + self.country_extra_pos]
        counties_to_update.append(country)

    def _update_state(self, item, all_states, states_to_update):
        state = all_states.filter(name=item['name']).first()
        state.state_code = item['state_code']
        state.latitude = item['latitude']
        state.longitude = item['longitude']
        states_to_update.append(state)

    def _update_city(self, item, all_cities, cities_to_update):
        city = all_cities.get(name=item['name'])
        city.latitude = item['latitude']
        city.longitude = item['longitude']
        cities_to_update.append(city)

    def _create_country_object(self, item, *args):
        base_model_fields = {
            'name': item[0 + self.country_extra_pos],
            'iso3': item[1 + self.country_extra_pos],
            'latitude': item[18 + self.country_extra_pos],
            'longitude': item[19 + self.country_extra_pos],
        }
        if "AbstactExpandedCountry" == models.Country.__bases__[0].__name__:
            base_model_fields.update({
                'iso2': item[2 + self.country_extra_pos],
                'numeric_code': item[3 + self.country_extra_pos],
                'phone_code': item[4 + self.country_extra_pos],
                'currency': item[7 + self.country_extra_pos],
                'currency_name': item[8 + self.country_extra_pos],
                'currency_symbol': item[9 + self.country_extra_pos]
            })

        return models.Country(**base_model_fields)

    def _create_state_object(self, item, country):
        return models.State(
            json_id=item['id'],
            name=item['name'],
            state_code=item['state_code'],
            latitude=item['latitude'],
            longitude=item['longitude'],
            country=country
        )

    def _create_city_object(self, item, state):
        return models.City(
            json_id=item['id'],
            name=item['name'],
            latitude=item['latitude'],
            longitude=item['longitude'],
            state=state
        )

    def _add_to_create_list(self, model, item, items_to_create, parent=None):
        item_creator = getattr(self, self.model_creator[model])
        items_to_create.append(item_creator(item, parent))

    def _get_buenos_aires_cities(self):
        response = requests.get(self.buenos_aires_data_url)
        if response.status_code != 200:
            raise Exception('Error getting data from url')
        response = json.loads(response.text)
        data = pd.DataFrame.from_dict(response['municipios'])
        cities = []
        for city in data.values:
            cities.append(
                {
                    'id':city[1],
                    'name':city[2],
                    'latitude':city[0]['lat'],
                    'longitude':city[0]['lon']
                }
            )
        return cities

    def handle(self, *args, **options):
        self._get_base_data_urls()
        st = time.time()
        """Handle the command."""
        data = self._get_data()

        all_countries = self._get_all_countries()
        all_countries_names = all_countries.values_list('name', flat=True)
        counties_to_create = []
        counties_to_update = []

        for item in data.values:
            if item[0 + self.country_extra_pos] not in all_countries_names:
                self._add_to_create_list('country', item, counties_to_create)
            else:
                self._update_country(item, all_countries, counties_to_update)

        if counties_to_create:
            print(f'Creating countries {len(counties_to_create)}')
            models.Country.objects.bulk_create(counties_to_create)
            print('Countries created')
        if counties_to_update:
            fields = self.extended_country_fields if \
                    "AbstactExpandedCountry" == models.Country.__bases__[0].__name__ \
                    else self.base_country_fields
            print(f'Updating countries {len(counties_to_update)}')
            models.Country.objects.bulk_update(counties_to_update, fields)
            print('Countries updated')

        if settings.get_user_setting('LOCATION_SCOPE') != 'country':
            states_to_create = []
            states_to_update = []
            for item in data.values:
                states_names_to_create = []
                country = all_countries.get(name=item[0 + self.extra_pos])
                all_country_states = country.states.all()
                all_country_states_names = all_country_states.values_list('name', flat=True)
                if not item[22 + self.extra_pos]:
                    item[22 + self.extra_pos] = [{
                            'id': 0,
                            'name': item[0 + self.extra_pos],
                            'state_code': item[1 + self.extra_pos],
                            'latitude': item[18 + self.extra_pos],
                            'longitude': item[19 + self.extra_pos],
                            'type':None
                            }]
                for state in item[22 + self.extra_pos]:
                    if state['type'] not in self.approved_state_types:
                        continue

                    if state['name'] not in all_country_states_names:
                        if state['name'] not in states_names_to_create:
                            self._add_to_create_list('state', state, states_to_create, country)
                            states_names_to_create.append(state['name'])
                    else:
                        self._update_state(state, all_country_states, states_to_update)

            if states_to_create:
                print(f'Creating states {len(states_to_create)}')
                try:
                    models.State.objects.bulk_create(states_to_create)
                    print('States created')
                except Exception as e:
                    print(e)
                    raise e
            if states_to_update:
                print(f'Updating states {len(states_to_update)}')
                models.State.objects.bulk_update(states_to_update, ['name', 'state_code', 'latitude', 'longitude'])
                print('States updated')

            if settings.get_user_setting('LOCATION_SCOPE') == 'city':
                all_cities_to_create = []
                all_cities_to_update = []
                for item in data.values:
                    country = all_countries.get(name=item[0 + self.extra_pos])
                    for state in item[22 + self.extra_pos]:
                        if state['type'] not in self.approved_state_types:
                            continue
                        if state['name'] == 'Buenos Aires':
                            state['cities'] = self._get_buenos_aires_cities()
                        cities_to_create = []
                        cities_to_update = []
                        cities_names_to_create = []
                        current_state = country.states.get(name=state['name'])
                        all_state_cities = current_state.cities.all()
                        all_state_cities_names = all_state_cities.values_list('name', flat=True)

                        if not state['cities'] and not all_state_cities:
                            state['cities'] = [{
                                'id': 0,
                                'name': state['name'],
                                'latitude': state['latitude'],
                                'longitude': state['longitude']
                            }]

                        for city in state['cities']:
                            if city['name'] not in all_state_cities_names:
                                if city['name'] not in cities_names_to_create:
                                    self._add_to_create_list('city', city, cities_to_create, current_state)
                                    cities_names_to_create.append(city['name'])
                            else:
                                self._update_city(city, all_state_cities, cities_to_update)

                        all_cities_to_create += cities_to_create
                        all_cities_to_update += cities_to_update

                if all_cities_to_create:
                    print(f'Creating cities {len(all_cities_to_create)}')
                    models.City.objects.bulk_create(all_cities_to_create)
                    print('Cities created')

                if all_cities_to_update:
                    print(f'Updating cities {len(all_cities_to_update)}')
                    models.City.objects.bulk_update(all_cities_to_update, ['name', 'latitude', 'longitude'])
                    print('Cities updated')

        # get the end time
        et = time.time()

        # get the execution time
        elapsed_time = et - st
        print('Execution time:', elapsed_time, 'seconds')