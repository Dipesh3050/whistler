# Generated by Django 4.2.6 on 2023-11-14 07:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Ride",
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
                ("employee_name", models.CharField(max_length=100)),
                ("total_seats", models.PositiveIntegerField(blank=True, null=True)),
                ("available_seats", models.PositiveIntegerField(blank=True, null=True)),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("passenger_location", models.CharField(max_length=100)),
                ("destination", models.CharField(max_length=100)),
                (
                    "passengers",
                    models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
                ),
            ],
        ),
        migrations.CreateModel(
            name="RideRequest",
            fields=[
                (
                    "req_id",
                    models.PositiveIntegerField(primary_key=True, serialize=False),
                ),
                (
                    "ride_status",
                    models.CharField(
                        choices=[
                            ("Approved", "Approved"),
                            ("Denied", "Denied"),
                            ("Requested", "Requested"),
                        ],
                        default="Requested",
                        max_length=10,
                    ),
                ),
                ("passengers", models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
                (
                    "ride",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="Lyft.ride"
                    ),
                ),
            ],
        ),
    ]