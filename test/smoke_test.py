__author__ = 'Ben Christenson'
__date__ = "2/9/16"
import sys
import unittest
sys.path.append(__file__.rsplit('/',3)[0])
from util import get_random_character_string, http_call

DEBUG_SERVER = 'http://127.0.0.1:4999'
LOCAL_SERVER = 'http://local.alienvault.benchristenson.com'
AWS_SERVER   = 'http://alienvault.benchristenson.com'

class AlienVaultTest(unittest.TestCase):
    SERVER = AWS_SERVER
    TRAFFIC_URL = '/api/traffic'
    THREAT_URL = '/api/threat/ip/%s'
    BURN_TEST_COUNT = 30
    BURN_TEST_START_IP = 16843009
    THREAT_IP = '69.43.161.174'
    SAFE_IP = '8.8.8.8'

    def test_traffic(self):
        """
            This will test the get method for /api/traffic
        """
        data = http_call(self.SERVER+self.TRAFFIC_URL)
        for d in data:
            assert 'alienvaultid' in d, 'Missing AlienVaultId'
            assert 'visits' in d, 'Missing visits'
            for v in d['visits']:
                assert isinstance(v.get('address',None), basestring), 'address missing or wrong type'
                assert isinstance(v.get('timestamp',None), int), 'timestamp missing or wrong type'
                assert isinstance(v.get('endpoint',None), basestring), 'endpoint missing or wrong type'

    def test_known_threat(self):
        """
            This will test an ip address that is a known threat
        """
        data = http_call(self.SERVER + self.THREAT_URL%self.THREAT_IP)
        self.validate_threat(threat=data)
        assert data['activities'], 'This should have activities since it is a known threat'

    def test_known_safe(self):
        """
            This will test an ip address that is known to be safe
        """
        data = http_call(self.SERVER + self.THREAT_URL%self.SAFE_IP)
        self.validate_threat(threat=data)

    def test_burn(self):
        """
            This will test "count" ip addresses starting at "index"
        """
        failures = {}
        index= self.BURN_TEST_START_IP
        for i in range(self.BURN_TEST_COUNT):
            index += 1
            ip = '%s.%s.%s.%s'%(int(index/(256*256*256)),
                                int(index/256*256)%256,
                                int(index/256)%256,
                                index%256)
            try:
                print 'Burn testing %s'%ip
                data = http_call(self.SERVER+self.THREAT_URL%ip)
                self.validate_threat(data)
            except Exception as e:
                failures[ip] = e
                print '     failure'
        if failures:
            raise

    def test_adding_cookie(self):
        """
            This will add a random cookie and make sure the visit was registered
        """
        data1 = http_call(self.SERVER+self.TRAFFIC_URL)
        http_call(self.SERVER+self.THREAT_URL%self.THREAT_IP)
        data2 = http_call(self.SERVER+self.TRAFFIC_URL)
        new_visit = [d for d in data2 if not d in data1][0]
        assert new_visit['visits'][0]['endpoint'] == self.THREAT_URL[1:]%self.THREAT_IP

        http_call(self.SERVER+self.THREAT_URL%self.SAFE_IP)
        data3 = http_call(self.SERVER+self.TRAFFIC_URL)
        new_visit = [d for d in data3 if not d in data2][0]
        assert new_visit['visits'][0]['endpoint'] == self.THREAT_URL[1:]%self.SAFE_IP

    def validate_threat(self, threat):
        for key in 'address id is_valid reputation_val activity_types ' \
                   'activities http_code invalid_activities_count'.split():
            assert key in threat, 'Missing %s from a threat report'%key

        for activity in threat['activities']:
            assert isinstance(activity.get('activity_type',None),basestring), 'Missing or bad activity_type'
            assert isinstance(activity.get('first_date',None),int), 'Missing or bad first_date'
            assert isinstance(activity.get('last_date',None),int), 'Missing or bad last_date'
            assert activity['first_date'] <= activity['last_date'], 'First was after last'
            assert activity['activity_type']  in threat['activity_types'], 'Missing activity type'







