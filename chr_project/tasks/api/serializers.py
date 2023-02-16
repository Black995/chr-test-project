from tasks.models import Location, Network, Station, Extra
from rest_framework import serializers
from django.db.models import F, Q



class LocationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Location
        fields = [
            "city",
            "country",
            "latitude",
            "longitude"
        ]


class NetworkSerializer(serializers.ModelSerializer):
    company = serializers.ListField(child=serializers.CharField())
    #company = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Network
        fields = [
            "id",
            "name",
            "href",
            "gbfs_href",
            "company",
            "location"           
        ]


class StationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Station
        fields = [
            "id",
            "name",
            "empty_slots",
            "free_bikes",
            "latitude",
            "longitude",
            "timestamp",
            "network"
        ]


class ExtraSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Extra
        fields = [
            "uid",
            "address",
            "altitude",
            "ebikes",
            "has_ebikes",
            "last_updated",
            "normal_bikes",
            "payment",
            "payment_terminal",
            "post_code",
            "renting",
            "returning",
            "slots",
            "station"
        ]
