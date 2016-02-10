"""
    These models are for storing tracking data of requests that have been made
"""

from django.db import models
import datetime
from util import get_random_character_string

ID_MAX_LENGTH = 12


class AlienVault(models.Model):
    """     This is essectially a user as recognized by a semi-unique cookie
        param created: Datetime of when the cookie was set
        param alien_vault_id: str of the semi-unique cookie
        param valid_count: int of the number of valid calls this user has done
        param total_count: int of the total number of call this user has done
        param error_count: int of the number of calls that had http errors
        """
    created = models.DateTimeField(auto_now_add=True)
    alien_vault_id = models.CharField(max_length=ID_MAX_LENGTH, default=get_random_character_string(ID_MAX_LENGTH))
    valid_count = models.IntegerField(default=0)
    total_count = models.IntegerField(default=0)
    error_count = models.IntegerField(default=0)


class TrackVisits(models.Model):
    """     This represents a single call for threat information
        param alien_vault: AlienVault of the user
        param address: str of the user's ip address when making the call
        param created: datetime of when the call was made
        param endpoint: str of the endpoint the user was calling
        """
    alien_vault = models.ForeignKey(AlienVault, related_name='visits')
    address = models.CharField(max_length=15)
    created = models.DateTimeField(auto_now_add=True)
    endpoint = models.CharField(max_length=50)

    @property
    def timestamp(self):
        """
        :return: int of the seconds since EPOCH that this call was created
        """
        return (self.created - datetime.datetime(1970,1,1,tzinfo=self.created.tzinfo)).total_seconds()