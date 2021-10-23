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

This method may not work because Zillow recognizes these requests are being sent using
AWS as a proxy. From the github page, "Please note that these requests can be easily identified 
and blocked, since they are sent with unique AWS headers (i.e. "X-Amzn-Trace-Id")".
"""

#This test will be with httpbin, which is great to test out what our header and ip look like
with ApiGateway("https://httpbin.org", access_key_id, access_key_secret) as g: #access_key_id and access_key_secret should be in the .env file. These arguments should be optional
    session = requests.Session()
    session.mount("https://httpbin.org", g)

    response = session.get("https://httpbin.org/anything")
    print(response.status_code)
    BeautifulSoup(response.content, "html.parser")
    #ip is the 'origin'. The first ip is the randomly generated 'X-My-X-Forwarded-For', the second ip is the proxy from AWS API Gateway



#New method: Tor
#*************************
"""
This method uses Tor to anonymize the IP address. This method requires Tor to be installed on your computer.
(On a mac with homebrew, you can run 'brew install tor'. When that's done you can start it with 'brew services run tor'.)
This method works at anonymizing the IP, but now Zillow recognizes the requests as a robot and throws a captcha.
Even if the header is exactly the same (besides X-Amzn_Trace-Id, which we can't control), the Tor method gets blocked 
while the regular requests method does not.
"""
import requests
header = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, sdch, br',
    'accept-language': 'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    "X-Amzn-Trace-Id": "Root=1-61743f40-2a15218e29d5244b14d3d3a2",
    'referer': 'https://www.google.com/'}

# Make a request through the Tor connection
# IP visible through Tor
session = requests.session()
session.proxies = {'http':  'socks5://127.0.0.1:9050',
                    'https': 'socks5://127.0.0.1:9050'}

#Get ip with Tor
response = session.get("http://httpbin.org/anything", headers=header)
response.status_code
BeautifulSoup(response.content, "html.parser")

#Test ip without Tor  (method that worked)
response = requests.get("http://httpbin.org/anything", headers=header)
response.status_code
BeautifulSoup(response.content, "html.parser")


#Test Zillow with Tor
response = session.get("http://zillow.com/Knoxville,-TN", headers=header)
response.status_code
BeautifulSoup(response.content, "html.parser") #Blocked by captcha

#Test Zillow without Tor
response = requests.get("http://zillow.com/Knoxville,-TN", headers=header)
response.status_code
BeautifulSoup(response.content, "html.parser") #Works




#We can use this code to test if a requests gets blocked by a captcha
"Please verify you're a human to continue" in str(BeautifulSoup(response.content, "html.parser"))
