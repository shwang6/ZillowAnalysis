from bs4 import BeautifulSoup
import requests
import json

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, sdch, br',
    'accept-language': 'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'referer': 'https://www.google.com/'
}
response = requests.get(
    'https://www.zillow.com/homedetails/1723-Brent-Hills-Blvd-Gatlinburg-TN-37738/81444371_zpid/', headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# Address
address = soup.find("meta", property="og:zillow_fb:address")
address['content']
# Beds
beds = soup.find("meta", property="zillow_fb:beds")
beds['content']
# Baths
baths = soup.find("meta", property="zillow_fb:baths")
baths['content']
# Description
description = soup.find("meta", property="zillow_fb:description")
description['content']
# Price
price = soup.find("meta", property="product:price:amount")
# price['content']
# JSON
data = json.loads(soup.find("script", type="application/ld+json").string)
data.keys()
data['@type']
data['name']  # Same as address
data['floorSize']['value']  # Sq. ft.
data['numberOfRooms']  # Same as bedrooms
data['address']  # Already broken down into pieces
data['geo']  # Latitude and longitude
# Bigger JSON

data = json.loads(soup.find("script", type="application/json",
                  id="hdpApolloPreloadedData").string)
data = json.loads(data['apiCache'])
data.keys()  # The keys got really wonky
# dict_keys(['VariantQuery{"zpid":81444371,"altId":null}',
#            'ForSaleDoubleScrollFullRenderQuery{"zpid":81444371,
#            "contactFormRenderParameter":{"zpid":81444371,"platform":"desktop","isDoubleScroll":true}}'])

# LOTS of good data
data['VariantQuery{"zpid":81444371,"altId":null}']['property'].keys()
data['VariantQuery{"zpid":81444371,"altId":null}']['property']['yearBuilt']
data['VariantQuery{"zpid":81444371,"altId":null}']['property']['lotSize']
data['VariantQuery{"zpid":81444371,"altId":null}']['property']['homeType']
data['VariantQuery{"zpid":81444371,"altId":null}']['property']['homeStatus']
data['VariantQuery{"zpid":81444371,"altId":null}']['property']['timeOnZillow']
data['VariantQuery{"zpid":81444371,"altId":null}']['property']['isPreforeclosureAuction']
data['VariantQuery{"zpid":81444371,"altId":null}']['property']['hoaFee']
data['VariantQuery{"zpid":81444371,"altId":null}']['property']['isZillowOwned']
data['VariantQuery{"zpid":81444371,"altId":null}']['property']['taxAssessedValue']
data['VariantQuery{"zpid":81444371,"altId":null}']['property']['lotAreaValue']
data['VariantQuery{"zpid":81444371,"altId":null}']['property']['lotAreaUnit']
data['VariantQuery{"zpid":81444371,"altId":null}']['property']['taxAssessedValue']

key2 = 'ForSaleDoubleScrollFullRenderQuery{"zpid":81444371,"contactFormRenderParameter":{"zpid":81444371,"platform":"desktop","isDoubleScroll":true}}'
data[key2]['property'].keys()
