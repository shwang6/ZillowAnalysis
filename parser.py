from io import TextIOWrapper
from typing import Dict, List, Union

# Parsing Imports
from bs4 import BeautifulSoup
import requests
import json
import time
from os import _exit
from os.path import exists

import firebase_admin
from firebase_admin import credentials, firestore


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Type Aliases to make Type Hints more helpful
URL = str
OpenFile = TextIOWrapper

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, sdch, br",
    "accept-language": "en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4",
    "cache-control": "max-age=0",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
    "referer": "https://www.google.com/",
}

class Parser:
    def __init__(self, data_source: Union[URL, None] = None) -> None:
        if isinstance(data_source, URL):
            response = requests.get(data_source, headers=headers).content

            self.soup = BeautifulSoup(response, "html.parser") if data_source else None

        self.urls: Dict[str, List[URL]] = {}
        self.listings: List[Dict] = []

        if exists('./parse_cache.json'):
            with open('parse_cache.json') as cache:
                self.parse_cache = json.load(cache)
        else:
            self.parse_cache: Dict[str, int] = {}



    def getListings(self, city: str, state: str, count: int) -> List[Dict]:
        listings = []
        count = int(count / 40)
        count += 1 if count == 0 else 0

        urls = self.parseSearchPage(city, state, [x for x in range(count)])
        url = 0

        while len(listings) < count:
            listings.append(urls[url])
            url += 1

        return listings

    def parseSearchPage(
        self, city_or_zip: str, state: str, pages: List[int] = []
    ) -> List[URL]:
        region = f"{city_or_zip},-{state}"
        search_url = f"https://www.zillow.com/{region}/"
        self.urls[region] = []
        if not pages:
            page = 1
            while (resp := requests.get(f"{search_url}{page}_p/")).status_code == 200:
                soup = BeautifulSoup(resp.content, "html.parser")
                # Get data from all listings
                all_listings = soup.find(
                    "script",
                    attrs={"data-zrr-shared-data-key": "mobileSearchPageStore"},
                ).string
                # Remove comment symbols
                all_listings = all_listings.replace("<!--", "")
                all_listings = all_listings.replace("-->", "")
                # Load in JSON format
                all_listings = json.loads(all_listings)["cat1"]["searchResults"][
                    "listResults"
                ]

                for listing in all_listings:
                    self.urls[region].append(listing["detailUrl"])

                page += 1
                # Sleep to prevent sending too many requests
                time.sleep(2)
        else:
            for page in pages:
                resp = requests.get(f"{search_url}{page}_p/", headers=headers)
                if resp.status_code == 400:
                    break
                soup = BeautifulSoup(resp.content, "html.parser")
                # Get data from all listings
                all_listings = soup.find(
                    "script",
                    attrs={"data-zrr-shared-data-key": "mobileSearchPageStore"},
                ).string
                # Remove comment symbols
                all_listings = all_listings.replace("<!--", "")
                all_listings = all_listings.replace("-->", "")
                # Load in JSON format
                all_listings = json.loads(all_listings)["cat1"]["searchResults"][
                    "listResults"
                ]

                for listing in all_listings:
                    self.urls[region].append(listing["detailUrl"])

                # Sleep to prevent sending too many requests
                time.sleep(2)

        return self.urls[region]

    def parseIndividalListing(self, url: URL) -> Dict:
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.content, "html.parser")

        data = json.loads(
            soup.find(
                "script", type="application/json", id="hdpApolloPreloadedData"
            ).string
        )
        data = json.loads(data["apiCache"])
        data = data[list(data.keys())[1]]

        listing_data = data["property"]
        self.listings.append(listing_data)

        return listing_data

    def parseListings(self, urls: List[URL]) -> List[Dict]:
        for url in urls:
            self.parseIndividalListing(url)["streetAddress"]
            time.sleep(1)
        return self.listings

    def getListingDataSP(
        self, c_or_z: str, st: str, pages: List[int] = [], rent: bool = False
    ) -> List[Dict]:
        """Gathers the listing data from a search page"""
        region = f"{c_or_z},-{st}"
        search_url = f"https://www.zillow.com/{region}/"
        if rent: search_url += 'rent/'
        these_listings = []
        start = self.parse_cache[region] if region in self.parse_cache else 1
        pages = [i for i in range(start, 21)] if not pages else pages
        all_addresses = set()

        for page in pages:
            try:
                resp = requests.get(f"{search_url}{page}_p/", headers=headers)
                soup = BeautifulSoup(resp.content, "html.parser")
                if all_listings := soup.find(
                    "script",
                    attrs={"data-zrr-shared-data-key": "mobileSearchPageStore"},
                ):
                    all_listings = all_listings.string.replace("<!--", "").replace(
                        "-->", ""
                    )
                    all_listings = json.loads(all_listings)["cat1"]["searchResults"][
                        "listResults"
                    ]
                    # If page redirected back to valid page break
                    if all_listings[0]['addressStreet'] in all_addresses: break
                    all_addresses = set()
                    for listing in all_listings:
                        if listing['addressStreet'] not in all_addresses:
                            self.saveListing(listing)
                            all_addresses.add(listing['addressStreet'])
                            these_listings.append(listing)

                time.sleep(1)
            except (ValueError):
                print(f'Capatcha encountered at {page} on {region}')
                self.parse_cache[region] = page
                with open('parse_cache.json', 'w') as cache:
                    cache.write(json.dumps(self.parse_cache))
                    _exit(1)

            self.parse_cache[region] = -1

        return these_listings

    def getZipCodes(self, start: str, amount: int = 50) -> List[str]:
        try:
            db_ref = db.collection('zipcodes').document(start)
            return [z.to_dict() for z in db.collection('zipcodes').start_at(db_ref.get()).limit(amount).get()]
        except:
            print(f'Zipcode for {start} not in DB')
            return []

    def saveListing(self, listing: Dict) -> bool:
        db.collection('listings').document(listing['zpid']).set(listing)
        return True


# Example of how to use class
if __name__ == "__main__":

    # Initialize Class
    parser = Parser()

    starting_zip = input('Starting ZipCode: ')
    count = input('Amount of ZipCodes to Parse: ')

    zip_codes = parser.getZipCodes(starting_zip, int(count))

    for zip_code in zip_codes:
        z = zip_code['Zipcode']
        st = zip_code['State']
        results = parser.getListingDataSP(z, st)
        print(f'Saved {len(results)} from {z} in {st}')
    # Loads First page of Search Results for Knoxville, TN
    # parser.getListingDataSP("37916", "TN")

    # Store list of data from houses

    # Urls are organized by Region
    # for listings in parser.urls.values():
    #     # Get data on the 3rd listing in the Region
    #     data = parser.parseListings(listings[:4])

    # # Prints some data about the first house
    # for home in data:
    #     print(f"House at {home['streetAddress']} was built in {home['yearBuilt']}" +
    #           f" and it was last sold for ${home['lastSoldPrice']}.")
