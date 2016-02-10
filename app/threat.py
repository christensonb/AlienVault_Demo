"""
    This module does http requests to the main server to get the status of known ip addresses

    # Known bad: 69.43.161.174
    # Known good: 8.8.8.8
    # Find more examples at https://www.alienvault.com/open-threat-exchange/dashboard
"""
__author__ = 'Ben Christenson'
__date__ = "2/8/16"

import urllib2
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
import serializers

class IPDetails(object):
    """
        This class does the http call and collates the data
    """
    def __init__(self, ip, *args, **kw):
        """
        :param ip: str of the ip address in the form of 1.22.333.444
        :param args: list of extra arguments, that are currently not being used
        :param kw: dict of extra arguments, that are currently not being used
        """
        # todo test that the ip is in range of 1-256
        raw, http_code = Reputation.get_details(ip)
        if raw and 200 <= http_code < 300:
            stream = BytesIO(raw)
            data = JSONParser().parse(stream)
            remote = serializers.RemoteDetailsSerializer(data=data)
            self.is_valid = remote.is_valid()
        else:
            self.is_valid = False
            data = {}

        try:
            self.http_code = http_code
            self.address = data.get('address',ip)
            self.id = data.get('id','')
            self.reputation_val = data.get('reputation_val',0)
            self.activities = [dict(activity_type=a['name'],
                                    first_date=a['first_date']['sec'],
                                    last_date=a['last_date']['sec']) for a in data.get('activities',[])
                                        if serializers.RemoteActivitiesSerializer(data=a).is_valid() ]
            self.invalid_activities_count = len(data.get('activities',[])) - len(self.activities)
            self.first_activity = self.get_activity(self.activities, 'first_date', less_than=True)
            self.last_activity = self.get_activity(self.activities, 'last_date', less_than=False)
            self.activity_types = list(set([a['activity_type'] for a in list(self.activities or [])]))
        except Exception as e:
            pass # todo more here one error handling

    @staticmethod
    def get_activity(activities, key, less_than=True):
        """
            This is used to get the first and last activity
        :param activities: list of dict containing <name, first_date, last_date
        :param key: str of the key to compare
        :param less_than: bool of True if it is to return the first activity
        :return: str of the name of the selected activity
        """
        if not activities:
            return None
        ret = activities[0]
        for activity in activities:
            if (activity[key] < ret[key]) == less_than:
                ret = activity
        return ret['activity_type']


class Reputation(object):
    @staticmethod
    def get_details(ip):
        """
            Gets the details on an ip address provided
            # -TODO: fetch raw results from the source
            #  format: http://reputation.us.alienvault.com/panel/ip_json.php?ip=69.43.161.174
            #  NOTE: the .us doesn't work

        :param ip: str of the ip address in the form of 1.22.333.444
        :return:   tuple (str <resulting call>, int <http code>)
                         resulting call which will be of a dict of <_id, address, reputation_val, status, ....>
        """
        if ip:
            try:
                url = "http://reputation.alienvault.com/panel/ip_json.php?ip=%s"%ip
                return urllib2.urlopen(url).read(), 200
            except urllib2.HTTPError, e:
                return "", e.code
        else:
            return "", 400