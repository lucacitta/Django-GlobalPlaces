import factory
from faker import Faker

from platform_configurations.models import City, State, Country

fake = Faker()

class CountryFactory(factory.Factory):
    class Meta:
        model = Country

    name = factory.LazyAttribute(lambda _: fake.unique.country())
    iso3 = factory.LazyAttribute(lambda _: fake.country_code())
    latitude = factory.LazyAttribute(lambda _: fake.latitude())
    longitude = factory.LazyAttribute(lambda _: fake.longitude())
    

class StateFactory(factory.Factory):
    class Meta:
        model = State

    json_id = factory.LazyAttribute(lambda _: fake.random_int())
    name = factory.LazyAttribute(lambda _: fake.unique.state())
    state_code = factory.LazyAttribute(lambda _: fake.state_abbr())
    latitude = factory.LazyAttribute(lambda _: fake.latitude())
    longitude = factory.LazyAttribute(lambda _: fake.longitude())
    country = factory.SubFactory(CountryFactory)


class CityFactory(factory.Factory):
    class Meta:
        model = City

    json_id = factory.LazyAttribute(lambda _: fake.random_int())
    name = factory.LazyAttribute(lambda _: fake.unique.city())
    latitude = factory.LazyAttribute(lambda _: fake.latitude())
    longitude = factory.LazyAttribute(lambda _: fake.longitude())
    state = factory.SubFactory(StateFactory)


def create_mundi_objects():
    """Funcion creada porque se rompe el por un unsaved raro. 
    No se puede usar el factory directamente por alguna razon"""
    country = CountryFactory.build()
    country.save()
    state = StateFactory.build(country=country)
    state.save()
    city = CityFactory.build(state=state)
    city.save()
    return country, state, city