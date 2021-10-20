from io import TextIOWrapper
from typing import Dict, List, Union, TypedDict

# Parsing Imports
from bs4 import BeautifulSoup
from urllib.parse import quote_plus
import requests
import json
import time

# Type Aliases to make Type Hints more helpful
URL = str
OpenFile = TextIOWrapper


class Listing(TypedDict):
    address: str
    url: str


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
    def __init__(self, data_source: Union[OpenFile, URL, None] = None) -> None:
        if isinstance(data_source, URL):
            response = requests.get(data_source, headers=headers).content
        elif isinstance(data_source, OpenFile):
            response = data_source.read()

        self.soup = BeautifulSoup(
            response, "html.parser") if data_source else None

        self.urls: Dict[str, List[URL]] = {}
        self.listings: List[Listing] = []

    def parseSearchPage(self, region: str, pages: List[int] = []) -> List[URL]:
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
                resp = requests.get(f'{search_url}{page}_p/', headers=headers)
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

    def parseIndividalListing(self, url: URL) -> Listing:
        pass


if __name__ == "__main__":
    parser = Parser()
    print(parser.parseSearchPage('Knoxville,-TN', [1, 2, 3]))
