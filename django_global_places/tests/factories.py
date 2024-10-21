import random
import string
import factory
from faker import Faker

from django_global_places.app_settings import api_settings as settings
from django_global_places.models import Country, City, State


fake = Faker()


class ShortCountryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Country

    name = factory.LazyAttribute(lambda _: fake.unique.country())
    iso3 = factory.Sequence(lambda n: "".join(random.sample(string.ascii_uppercase, 3)))
    latitude = factory.LazyAttribute(lambda _: fake.latitude())
    longitude = factory.LazyAttribute(lambda _: fake.longitude())
    is_active = factory.LazyAttribute(lambda _: True)

class ExpandedCountryFactory(ShortCountryFactory):
    iso2 = factory.Sequence(lambda n: "".join(random.sample(string.ascii_uppercase, 2)))
    numeric_code = factory.LazyAttribute(lambda _: fake.unique.random_int(min=100, max=999))
    phone_code = factory.LazyAttribute(lambda _: fake.random_int(min=1, max=999))
    currency = factory.LazyAttribute(lambda _: fake.currency_code())
    currency_name = factory.LazyAttribute(lambda _: fake.word())
    currency_symbol = factory.LazyAttribute(lambda _: fake.word())


CountryFactory = ShortCountryFactory if not settings.get_user_setting('INCLUDE_EXPANDED_COUNTRY') else ExpandedCountryFactory


class StateFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = State

    json_id = factory.LazyAttribute(lambda _: fake.random_int())
    name = factory.LazyAttribute(lambda _: fake.state())
    state_code = factory.LazyAttribute(lambda _: fake.state_abbr())
    latitude = factory.LazyAttribute(lambda _: fake.latitude())
    longitude = factory.LazyAttribute(lambda _: fake.longitude())
    country = factory.SubFactory(CountryFactory)


class CityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = City

    json_id = factory.LazyAttribute(lambda _: fake.random_int())
    name = factory.LazyAttribute(lambda _: fake.unique.city())
    latitude = factory.LazyAttribute(lambda _: fake.latitude())
    longitude = factory.LazyAttribute(lambda _: fake.longitude())
    state = factory.SubFactory(StateFactory)

