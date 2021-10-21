from io import TextIOWrapper
from typing import Dict, List, Union

# Parsing Imports
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import requests
import json
import time

from helpers.headers import getRandomHeaders

# Type Aliases to make Type Hints more helpful
URL = str
OpenFile = TextIOWrapper

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, sdch, br',
    'accept-language': 'en-GB,en;q=0.8,en-US;q=0.6,ml;q=0.4',
    'cache-control': 'max-age=0',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
    'referer': 'https://www.google.com/'
}


class Parser():
    def __init__(self, data_source: Union[URL, None] = None) -> None:
        if isinstance(data_source, URL):
            response = requests.get(data_source, headers=headers).content

        self.soup = BeautifulSoup(
            response, "html.parser") if data_source else None

        self.urls: Dict[str, List[URL]] = {}
        self.listings: List[Dict] = []

    def parseSearchPage(self, city: str, state: str, pages: List[int] = []) -> List[URL]:
        region = f'{city},-{state}'
        search_url = f'https://www.zillow.com/{region}/'
        self.urls[region] = []
        if not pages:
            page = 1
            while (resp := requests.get(f'{search_url}{page}_p/', headers=headers)).status_code == 200:
                soup = BeautifulSoup(resp.content, "html.parser")
                # Get data from all listings
                all_listings = soup.find(
                    'script', attrs={"data-zrr-shared-data-key": "mobileSearchPageStore"}).string
                # Remove comment symbols
                all_listings = all_listings.replace('<!--', '')
                all_listings = all_listings.replace('-->', '')
                # Load in JSON format
                all_listings = json.loads(all_listings)[
                    'cat1']['searchResults']['listResults']

                for listing in all_listings:
                    self.urls[region].append(listing['detailUrl'])

                page += 1
                # Sleep to prevent sending too many requests
                time.sleep(2)
        else:
            for page in pages:
                resp = requests.get(
                    f'{search_url}{page}_p/', headers=headers)
                if resp.status_code == 400:
                    break
                soup = BeautifulSoup(resp.content, "html.parser")
                # Get data from all listings
                all_listings = soup.find(
                    'script', attrs={"data-zrr-shared-data-key": "mobileSearchPageStore"}).string
                # Remove comment symbols
                all_listings = all_listings.replace('<!--', '')
                all_listings = all_listings.replace('-->', '')
                # Load in JSON format
                all_listings = json.loads(all_listings)[
                    'cat1']['searchResults']['listResults']

                for listing in all_listings:
                    self.urls[region].append(listing['detailUrl'])

                # Sleep to prevent sending too many requests
                time.sleep(2)

        return self.urls[region]

    def parseIndividalListing(self, url: URL) -> Dict:
        resp = requests.get(url, headers=headers)
        soup = BeautifulSoup(resp.content, "html.parser")

        data = json.loads(soup.find("script", type="application/json",
                                    id="hdpApolloPreloadedData").string)
        data = json.loads(data['apiCache'])
        data = data[list(data.keys())[1]]

        listing_data = data['property']
        self.listings.append(listing_data)

        return listing_data

    def parseListings(self, urls: List[URL]) -> List[Dict]:
        for url in urls:
            self.parseIndividalListing(url)["streetAddress"]
            time.sleep(1)
        return self.listings


# Example of how to use class
if __name__ == "__main__":

    # Initialize Class
    parser = Parser()

    # Loads First page of Search Results for Knoxville, TN
    parser.parseSearchPage('Knoxville', 'TN', [1])

    # Store list of data from houses
    data = []

    # Urls are organized by Region
    for listings in parser.urls.values():
        # Get data on the 3rd listing in the Region
        data = parser.parseListings(listings[:4])

    # Prints some data about the first house
    for home in data:
        print(f"House at {home['streetAddress']} was built in {home['yearBuilt']}" +
              f" and it was last sold for ${home['lastSoldPrice']}.")
