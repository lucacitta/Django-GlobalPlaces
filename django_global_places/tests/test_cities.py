import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from django_global_places.tests.factories import CityFactory
from django_global_places.utils import use_default_city_model, get_abstract_city_model


@pytest.mark.skipif(not get_abstract_city_model() or not use_default_city_model(),
                    reason="Skipping because custom city model is used")
@pytest.mark.django_db
class TestCityViewSet:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        # Create initial cities
        CityFactory.create(name='Los Angeles')
        CityFactory.create(name='Houston')
        CityFactory.create(name='New York')

    def test_list_cities(self):
        CityFactory.create_batch(2)

        url = reverse('cities-list')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 5  # Verify that the number of cities is 5

    def test_search_city(self):
        url = reverse('cities-list')

        # Search by name
        response = self.client.get(url, {'search': 'Houston'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["name"] == 'Houston'

        # Search that should return multiple results
        response = self.client.get(url, {'search': 'e'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2  # Los Angeles and New York
        assert sorted([result["name"] for result in response.data["results"]]) == ['Los Angeles', 'New York']

        # Search that returns no results
        response = self.client.get(url, {'search': 'NotACity'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0

    def test_ordering_cities(self):
        url = reverse('cities-list')

        response = self.client.get(url, {'ordering': 'name'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 3
        assert response.data["results"][0]["name"] == 'Houston'
        assert response.data["results"][1]["name"] == 'Los Angeles'
        assert response.data["results"][2]["name"] == 'New York'

        response = self.client.get(url, {'ordering': '-name'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 3
        assert response.data["results"][0]["name"] == 'New York'
        assert response.data["results"][1]["name"] == 'Los Angeles'
        assert response.data["results"][2]["name"] == 'Houston'

    def test_retrieve_city_fields(self):
        city = CityFactory.create()
        url = reverse('cities-detail', kwargs={'pk': city.pk})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == city.name

