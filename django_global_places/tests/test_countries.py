import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from django_global_places.app_settings import api_settings as settings
from django_global_places.tests.factories import CountryFactory
from django_global_places.utils import use_default_country_model, get_abstract_country_model


@pytest.mark.skipif(not get_abstract_country_model or not use_default_country_model(), 
                    reason="Skipping because custom country model is used")
@pytest.mark.django_db
class TestCountryViewSet:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        CountryFactory.create(name='Argentina', iso3='ARG')
        CountryFactory.create(name='Brazil', iso3='BRA')
        CountryFactory.create(name='Mexico')

    def test_list_countries(self):
        CountryFactory.create_batch(2)

        url = reverse('countries-list') 
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 5  # Verify that the number of countries is 5

    def test_search_country(self):
        url = reverse('countries-list')

        # Search by name
        response = self.client.get(url, {'search': 'Mexico'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["name"] == 'Mexico'

        # Search by ISO3
        response = self.client.get(url, {'search': 'ARG'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["name"] == 'Argentina'

        # Search that should return multiple results
        response = self.client.get(url, {'search': 'a'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2  # Argentina and Brazil
        assert sorted([result["name"] for result in response.data["results"]]) == ['Argentina', 'Brazil']

        # Search that returns no results
        response = self.client.get(url, {'search': 'NotACountry'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0

    def test_ordering_countries(self):
        url = reverse('countries-list')

        response = self.client.get(url, {'ordering': 'name'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 3
        assert response.data["results"][0]["name"] == 'Argentina'
        assert response.data["results"][1]["name"] == 'Brazil'

        response = self.client.get(url, {'ordering': '-name'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 3
        assert response.data["results"][0]["name"] == 'Mexico'
        assert response.data["results"][1]["name"] == 'Brazil'
    
    def test_retrieve_country_fields(self):
        country = CountryFactory.create()
        url = reverse('countries-detail', kwargs={'pk': country.pk})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == country.name
        assert response.data['iso3'] == country.iso3

    @pytest.mark.parametrize("field", ['iso2', 'numeric_code', 'phone_code', 'currency', 'currency_name', 'currency_symbol'])
    def test_include_expanded_country(self, field):
        country = CountryFactory.create()
        url = reverse('countries-detail', kwargs={'pk': country.pk})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK

        use_expanded_country = settings.get_user_setting('INCLUDE_EXPANDED_COUNTRY')

        if use_expanded_country:
            assert field in response.data, f"{field} should be in the response when INCLUDE_EXPANDED_COUNTRY is enabled"
        else:
            assert field not in response.data, f"{field} should not be in the response when INCLUDE_EXPANDED_COUNTRY is disabled"
        
