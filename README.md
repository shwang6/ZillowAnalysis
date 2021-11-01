# Zillow Project
This project is to retrieve data from Zillow and analyze trends in the housing market.

## Task List:
Create master function (see sudo-code below)   
Get function to run on virtual machines   
Implement auto-start/top of VM when code gets blocked   
+ Update parser to return search results, not just individual listings
+ Update parser to accept zip code as input
+ Update parser return rental results


## Master Function Sudo-Code

1. Get zip code from Firestore that has not yet been scraped (see 'firestore_examples.py')
2. Get random user-agent for heading
3. If http request was not blocked by captcha:
4. Get range of page results (for the for-loop below)      
   (Number of pages is the number of results/40, with a max of 25)   
5. For each page in search results:   
    a. Parse and clean response (clean_results.py)   
    b. For each listing in search results:    
            i. Add to Firestore 'listings' collection (see 'firestore_examples.py')   
6. Repeat with rentals = True (append '/rentals' to URL)
7. Update zip code in Firestore with 'scraped' = True







