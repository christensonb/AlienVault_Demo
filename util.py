"""
    This module holds generic functions
"""
__author__ = 'Ben Christenson'
__date__ = "2/8/16"
import urllib2
import requests
import json
import time
from random import random, seed
from string import digits, letters
CHARACTERS = digits + letters
seed(time.time())

def get_ip(request):
    """
        This will get the users IP address
    :param request: Request of the caller
    :return: str of the ip address in the form of 1.22.333.444
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_random_character_string(length=12):
    """
    :param length: int of the length of the characters
    :return: returns a unique string of "length" characters
    """
    return ''.join([CHARACTERS[int(random()*len(CHARACTERS))] for i in range(length)])

def http_call(url, cookies=None):
    """
    :param url: str of the url to call
    :param cookies: dict of cookies to call with
    :return: dict of the returned data
    """
    if cookies:
        raw = requests.get(url,cookies=cookies).content
    else:
        raw = urllib2.urlopen(url).read()

    data = json.loads(raw)
    return data