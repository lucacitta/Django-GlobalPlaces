import pytest
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from django_global_places.tests.factories import StateFactory
from django_global_places.utils import use_default_state_model, get_abstract_state_model


@pytest.mark.skipif(not get_abstract_state_model() or not use_default_state_model(),
                    reason="Skipping because custom state model is used")
@pytest.mark.django_db
class TestStateViewSet:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.client = APIClient()
        # Create initial states
        StateFactory.create(name='California', state_code='CA')
        StateFactory.create(name='Texas', state_code='TX')
        StateFactory.create(name='New York', state_code='NY')

    def test_list_states(self):
        StateFactory.create_batch(2)

        url = reverse('states-list')
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 5  # Verify that the number of states is 5

    def test_search_state(self):
        url = reverse('states-list')

        # Search by name
        response = self.client.get(url, {'search': 'California'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["name"] == 'California'

        # Search by code
        response = self.client.get(url, {'search': 'TX'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["name"] == 'Texas'

        # Search that should return multiple results
        response = self.client.get(url, {'search': 'a'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2 
        assert sorted([result["name"] for result in response.data["results"]]) == ['California', 'Texas']

        # Search that returns no results
        response = self.client.get(url, {'search': 'NotAState'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 0

    def test_ordering_states(self):
        url = reverse('states-list')

        response = self.client.get(url, {'ordering': 'name'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 3
        assert response.data["results"][0]["name"] == 'California'
        assert response.data["results"][1]["name"] == 'New York'
        assert response.data["results"][2]["name"] == 'Texas'

        response = self.client.get(url, {'ordering': '-name'})
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 3
        assert response.data["results"][0]["name"] == 'Texas'
        assert response.data["results"][1]["name"] == 'New York'
        assert response.data["results"][2]["name"] == 'California'

    def test_retrieve_state_fields(self):
        state = StateFactory.create()
        url = reverse('states-detail', kwargs={'pk': state.pk})
        response = self.client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == state.name
        assert response.data['state_code'] == state.state_code

        