# Generated by Django 5.0.6 on 2024-05-27 12:24

import django.db.models.deletion
from django.db import migrations, models

from django_global_places.app_settings import api_settings as settings


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Country",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100, unique=True)),
                ("iso3", models.CharField(max_length=3)),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
                ("is_active", models.BooleanField(default=True)),
            ],
            options={
                "verbose_name_plural": "Countries",
            },
        ),
        migrations.CreateModel(
            name="State",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("json_id", models.IntegerField()),
                ("name", models.CharField(max_length=100)),
                ("state_code", models.CharField(max_length=5)),
                ("latitude", models.FloatField(blank=True, null=True)),
                ("longitude", models.FloatField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "country",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="states",
                        to="django_global_places.country",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "States",
            },
        ),
        migrations.CreateModel(
            name="City",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("json_id", models.IntegerField()),
                ("name", models.CharField(max_length=100)),
                ("latitude", models.FloatField(blank=True, null=True)),
                ("longitude", models.FloatField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "state",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cities",
                        to="django_global_places.state",
                    ),
                ),
            ],
            options={
                "verbose_name_plural": "Cities",
            },
        ),
    ]
