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
"""

# Create gateway object and initialise in AWS
gateway = ApiGateway("https://www.zillow.com")
gateway.start()

# Assign gateway to session
session = requests.Session()
session.mount("https://www.zillow.com", gateway)

# Send request (IP will be randomised)
url= 'https://www.zillow.com/homes/Knoxville-TN/'
response = session.post(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.1.1 Safari/605.1.15',
                                                                 "X-My-X-Forwarded-For":"29.391.493.29"})
# We will also need to rotate the 'User-Agent' and maybe randomize the X-My-X-Fowarded-For
print(response.status_code)

# Delete gateways
gateway.shutdown()
