# coding=utf-8
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status
import datetime
import settings
from util import get_ip

from threat import IPDetails
from models import AlienVault, TrackVisits
from serializers import *

class APIRoot(APIView):
    def get(self, request):
        return Response({
            'IP Details': reverse('threat_details', request=request),
        })

class IPDetailsView(APIView):
    """
        Views for the url: api/threat/ip/1.2.3.4
           1) Make a simple Web API using Django Rest Framework (http://www.django-rest-framework.org/)in Python that can take any IP as input. URL format: /api/threat/ip/x.x.x.x as the format. Provide reasonable error­checking for IP input (empty, invalid, etc.)
           2) Map the information from reputation.alienvault.com to this output API
           3) See right column in first table on how to handle an error where no results are returned. I’ve included an is_valid field to set true or false on bad input. Feel free to add any API fields you think are relevant (error codes, etc.)
           4) On a user access to the API, determine if it is their first access by looking to see if they have a cookie set for a unique user ID (call it AlienvaultID). If they do not have a cookie set, set it to a random string to 12 characters and set it to expire in one year.
               (Yes, this isn’t totally scientific but it simulates the behavior of many marketing automation packages.)
    """
    def get(self, request, ip, *args, **kw):
        """
        :param ip: str of the ip address the user wants a threat report for
        :return: IPDetails
        """
        ip_details = IPDetails(ip, *args, **kw)
        serialize = DetailsSerializer(ip_details)
        response = Response(serialize.data, status=status.HTTP_200_OK)

        cookie = request.COOKIES.get(settings.COOKIE_NAME, None)
        if  cookie is None:
            alien_vault = AlienVault()
        else:
            try:
                alien_vault = AlienVault.objects.filter(alien_vault_id=cookie).get()
            except:
                alien_vault = AlienVault()

        alien_vault.total_count += 1
        alien_vault.valid_count += ip_details.is_valid and 1 or 0
        alien_vault.error_count += ip_details.http_code > 299 and 1 or 0
        alien_vault.save()

        TrackVisits(alien_vault=alien_vault,
                    address = get_ip(request),
                    endpoint='api/threat/ip/%s'%ip).save()

        expires = datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.COOKIE_LIFETIME)
        response.set_cookie(settings.COOKIE_NAME,
                            alien_vault.alien_vault_id,
                            max_age=settings.COOKIE_LIFETIME,
                            expires=expires.strftime('%a, %d-%b-%Y %H:%M:%S GMT'),
                            domain=settings.COOKIE_DOMAIN,
                            secure = settings.COOKIE_SECURE or None)

        return response

class TrackVisitsView(APIView):
    """
        Views for the url: api/traffic
            1) Create a Django model to track simple statistics about who accesses the API via the web.
                a) IP Address
                b) Timestamp (epoch)
                c) API endpoint accessed ("/api/threat/ip/1.2.3.4")
                d) The value of AlienvaultID set in #4 in the previous section
            2) On each visit to the API endpoint above, record statistics about the user visiting.
            3) Create another API endpoint using DRF at /api/traffic/ that does a simple dump of all the traffic
            stored in the model above sorted by AlienvaultID.
    """

    def get(self, request):
        """
        :return: list of user's alienvaultid with each of their visits
        """
        alien_vaults = AlienVault.objects.order_by('alien_vault_id').select_related().all()
        serialize = AlienVaultSerializer(alien_vaults, many=True)
        response = Response(serialize.data)
        return response












