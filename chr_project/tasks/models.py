from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MaxValueValidator, MinValueValidator




class Location(models.Model):
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=50)
    latitude = models.FloatField(
        default=0,
        validators=[
            MaxValueValidator(180),
            MinValueValidator(-180)
        ]
    )
    longitude = models.FloatField(
        default=0,
        validators=[
            MaxValueValidator(180),
            MinValueValidator(-180)
        ]
    )


class Network(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    href = models.CharField(max_length=200)
    gbfs_href = models.CharField(max_length=200)
    company = ArrayField(
        models.CharField(max_length=50, blank=True)
    )
    location = models.OneToOneField(Location, null=True, 
                                    related_name='location_network', on_delete=models.SET_NULL)


class Station(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    name = models.CharField(max_length=100)
    empty_slots = models.IntegerField(default=0)
    free_bikes = models.IntegerField(default=0)
    latitude = models.FloatField(
        default=0,
        validators=[
            MaxValueValidator(180),
            MinValueValidator(-180)
        ]
    )
    longitude = models.FloatField(
        default=0,
        validators=[
            MaxValueValidator(180),
            MinValueValidator(-180)
        ]
    )
    timestamp = models.DateTimeField()
    network = models.ForeignKey(Network, related_name='network_station', on_delete=models.CASCADE)


class Extra(models.Model):
    uid = models.IntegerField(primary_key=True)
    address = models.CharField(max_length=100)
    altitude = models.FloatField(default=0)
    ebikes = models.IntegerField(default=0)
    has_ebikes = models.BooleanField()
    last_updated = models.IntegerField()
    normal_bikes = models.IntegerField(default=0)
    payment = ArrayField(
        models.CharField(max_length=50, blank=True)
    )
    payment_terminal = models.BooleanField()
    post_code = models.CharField(max_length=10, null=True)
    renting = models.IntegerField(default=0)
    returning = models.IntegerField(default=0)
    slots = models.IntegerField(default=0)
    station = models.OneToOneField(Station, null=True,
                                        related_name='station_extra', on_delete=models.SET_NULL)
