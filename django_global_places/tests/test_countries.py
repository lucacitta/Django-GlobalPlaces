import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from django_global_places.app_settings import api_settings as settings
from django_global_places.tests.factories import CountryFactory, StateFactory, CityFactory
from django_global_places.utils import use_default_country_model, use_default_state_model, use_default_city_model,\
    get_abstract_country_model, get_abstract_state_model, get_abstract_city_model


@pytest.mark.skipif(not get_abstract_country_model or not use_default_country_model(), 
                    reason="Skipping because custom country model is used")
@pytest.mark.django_db
class TestCountryViewSet:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()

    def test_list_countries(self):
        CountryFactory.create_batch(5)

        url = reverse('countries-list') 
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 5  # Verify that the number of countries is 5


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


@pytest.mark.skipif(not get_abstract_state_model() or not use_default_state_model(),
                    reason="Skipping because custom state model is used")
@pytest.mark.django_db
class TestStateViewSet:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()

    def test_list_states(self):
        StateFactory.create_batch(5)

        url = reverse('states-list')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 5

    
    def test_retrieve_state(self):
        state = StateFactory.create()

        url = reverse('states-detail', kwargs={'pk': state.pk})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == state.name
        assert response.data['state_code'] == state.state_code

    
@pytest.mark.skipif(not get_abstract_city_model() or not use_default_city_model(),
                    reason="Skipping because custom city model is used")
@pytest.mark.django_db
class TestCityViewSet:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()

    def test_list_cities(self):
        CityFactory.create_batch(5)

        url = reverse('cities-list')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 5

    
    def test_retrieve_city(self):
        city = CityFactory.create()

        url = reverse('cities-detail', kwargs={'pk': city.pk})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == city.name
        assert response.data['state'] == city.state.id
        
