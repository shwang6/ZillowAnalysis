import random

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, sdch, br',
    'accept-language': 'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'referer': 'https://www.google.com/'
}


# A User-Agent string in the request header helps to identify 
# the information of browser and operating system from which request has been executed.

# Every requests made contains some header information. User-agent is one of them and
# leads to the detection of the bot. User-agent rotation helps prevent getting caught. 

# Most websites don't allow multiple requests from a single source, so randomizing the
# user-agent while making a request will attempt to change the identity.


# Desktop User Agents
user_agents = [
# Sample user-agent string
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
# Windows 10-based PC using Edge browser
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246',
# Chrome OS-based laptop using Chrome browser (Chromebook)
'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
# Mac OS X-based computer using a Safari browser
'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
# Windows 7-based PC using a Chrome browser
'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.111 Safari/537.36',
# Linux-based PC using a Firefox browser
'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1',
# Chrome UA string
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
# Opera UA string
'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41',
# Microsoft Edge UA string
'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.59',
# Firefox UA string
'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',
]

# Random Function
# Generate a random user-agent from the ones in the user_agents list
def randomUserAgent():
    return random.choice(user_agents)

# Return headers with random user agent string
def getRandomHeaders():
    headers['user-agents'] = randomUserAgent()
    return headers



