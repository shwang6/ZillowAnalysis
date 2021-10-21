import requests
from requests_ip_rotator import ApiGateway
import pprint
import pickle
from bs4 import BeautifulSoup
import json

"""
We want to be able to rotate IP addresses to prevent Zillow from blocking the web crawler.
There are publicly available proxies that aren't very reliable because they're public.
This method uses proxies from AWS API Gateway. Docs at https://github.com/Ge0rg3/requests-ip-rotator

There has been a recent update to this function that makes the code much more condensed,
automatically starts and shuts off the gateway (so we don't get accidental charges from AWS),
and automatically radomizes the 'X-My-X-Forwarded-For'.
Make sure you have the latest version 1.0.10 with 'pip3 install requests-ip-rotator --upgrade'.
"""

#This test will be with httpbin, which is great to test out what our header and ip look like
with ApiGateway("https://httpbin.org", access_key_id, access_key_secret) as g: #access_key_id and access_key_secret should be in the .env file. These arguments should be optional
    session = requests.Session()
    session.mount("https://httpbin.org", g)

    response = session.get("https://httpbin.org/anything")
    print(response.status_code)
    BeautifulSoup(response.content, "html.parser")
    #ip is the 'origin'. The first ip is the randomly generated 'X-My-X-Forwarded-For', the second ip is the proxy from AWS API Gateway