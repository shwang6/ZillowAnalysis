# Zillow Project
This project is to retrieve data from Zillow and analyze trends in the housing market.

## Task List:
Successfully scrape Zillow web page
+ Two methods: 
 	- 1. Scrape search results page of many listings
 	- 2. Scrape individual pages, looping through every link in results
+ Implement IP rotations
+ Implement user-agent rotations
+ Maybe: use official Zillow API
+ Alternative data source: Zillow's downloadable market data
  - MUCH more limited; data already filtered and aggregated
  - https://www.zillow.com/research/data/
+ Parse response

Put web scraper inside a working function
+ Accepts either a city name or zip code
+ Returns data frame with every property’s attributes
 	- One row for each property
+ Stretch goal: argument to specify if you want for-sale properties or rental properties

Integrate Google Cloud for Data Storage
+ Automate data entry to upload to Google Cloud with each web crawl

New attributes/features
+ Mine description for more details
+ Stretch goal: enrich data with school district, crime rates, walkability, etc. (probably from another source)
