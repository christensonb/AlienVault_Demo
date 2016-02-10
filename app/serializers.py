from rest_framework import serializers
from models import AlienVault, TrackVisits

class RemoteDateSerializer(serializers.Serializer):
    usec = serializers.IntegerField()
    sec = serializers.IntegerField()


class RemoteActivitiesSerializer(serializers.Serializer):
    name = serializers.CharField()
    first_date = RemoteDateSerializer()
    last_date = RemoteDateSerializer()


class RemoteDetailsSerializer(serializers.Serializer):
    # -TODO: serialize the rest of your values in IPDetails here
    _id = serializers.CharField(required=True,source='_id.$id')
    status = serializers.BooleanField(required=True)
    activities = RemoteActivitiesSerializer(many=True)
    address = serializers.CharField()
    reputation_val = serializers.IntegerField(default=0)

    #       the following are other parameters returned, that we don't care about
    # allow_ping = serializers.CharField()
    # server_type = serializers.Field()
    # lon = serializers.Field()
    # up = serializers.Field()
    # reputation_rel = serializers.Field()
    # matched_wl = serializers.Field()
    # domains = serializers.Field()
    # _as = serializers.Field(source = 'as')
    # matched_bl = serializers.Field()
    # reputation_rel_checked = serializers.Field()
    # lat = serializers.Field()
    # reputation_val_checked = serializers.IntegerField()


class ActivitiesSerializer(serializers.Serializer):
    activity_type = serializers.CharField()
    first_date =  serializers.IntegerField()
    last_date =  serializers.IntegerField()


class DetailsSerializer(serializers.Serializer):
    address = serializers.CharField()
    id = serializers.CharField()
    is_valid = serializers.BooleanField()
    reputation_val = serializers.IntegerField()
    activity_types = serializers.ListField(child=serializers.CharField())
    activities = ActivitiesSerializer(many=True)
    http_code = serializers.IntegerField()
    invalid_activities_count = serializers.IntegerField()


class VisitsSerializers(serializers.Serializer):
    address = serializers.CharField()
    timestamp = serializers.IntegerField()
    endpoint = serializers.CharField()


class AlienVaultSerializer(serializers.Serializer):
    alienvaultid = serializers.CharField(source='alien_vault_id')
    visits = VisitsSerializers(many=True)

