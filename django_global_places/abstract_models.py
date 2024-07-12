from django.db import models

from django_global_places.app_settings import api_settings as settings

#<-------------- Places -------------->


class AbstactCountry(models.Model):
    name = models.CharField(max_length=100, unique=True)
    iso3 = models.CharField(max_length=3)
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class AbstactExpandedCountry(AbstactCountry):
    iso2 = models.CharField(max_length=2, null=True, blank=True)
    numeric_code = models.CharField(max_length=3, null=True, blank=True)
    phone_code = models.CharField(max_length=3, null=True, blank=True)
    currency = models.CharField(max_length=3, null=True, blank=True)
    currency_name = models.CharField(max_length=100, null=True, blank=True)
    currency_symbol = models.CharField(max_length=3, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class AbstractState(models.Model):
    json_id = models.IntegerField()
    name = models.CharField(max_length=100)
    state_code = models.CharField(max_length=5)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    country = models.ForeignKey(settings.get_user_setting('COUNTRY_MODEL'), on_delete=models.CASCADE, related_name='states')
    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class AbstractCity(models.Model):
    json_id = models.IntegerField()
    name = models.CharField(max_length=100)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    state = models.ForeignKey(settings.get_user_setting('STATE_MODEL'), on_delete=models.CASCADE, related_name='cities')

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


#<-------------- Locations -------------->