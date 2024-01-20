from django.contrib import admin
from django.conf import settings

from platform_configurations import models
from django_base.base_utils.utils import (
    get_abstract_state_model,
    get_abstract_city_model
)

if settings.INCLUDE_LOCATION:

    @admin.register(models.Country)
    class CountryAdmin(admin.ModelAdmin):
        list_display = ('pk', 'name', 'iso3', 'latitude', 'longitude')
        search_fields = ('pk', 'name', 'iso3', 'latitude', 'longitude')
        list_filter = ("is_active",)

    if get_abstract_state_model():
        @admin.register(models.State)
        class StateAdmin(admin.ModelAdmin):
            list_display = ('pk', 'name', 'state_code', 'latitude', 'longitude')
            search_fields = ('pk', 'name', 'state_code', 'latitude', 'longitude')
            list_filter = ('is_active', 'country',)

    if get_abstract_city_model():
        @admin.register(models.City)
        class CityAdmin(admin.ModelAdmin):
            list_display = ('pk', 'name', 'latitude', 'longitude')
            search_fields = ('pk', 'name', 'latitude', 'longitude')
            list_filter = ('is_active', 'state',)