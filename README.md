# Zillow Project
This project is to retrieve data from Zillow and analyze trends in the housing market.

## Task List:
+ Create master function (see pseudocode below)   
   + Update parser to return search results, not just individual listings
   + Update parser to accept zip code as input
   + Update parser return rental results
+ Get function to run on virtual machines   
+ Implement auto-start/top of VM when code gets blocked   



## Master Function Pseudocode

1. Get zip code from Firestore that has not yet been scraped (see 'firestore.py')
2. Get random user-agent for heading (headers.py)
3. Get first page of search results
4. If http request was not blocked by captcha:    
&nbsp;&nbsp;&nbsp;&nbsp;a. Get range of page results (for the for-loop below)      
   (Number of pages is the number of results/40, with a max of 25)   
&nbsp;&nbsp;&nbsp;&nbsp; b. For each page in search results (starting with page 2):   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    i. If http request was no blocked:   
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 1. Parse and clean response (clean_results.py)    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; 2. For each listing in search results:    
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; a. Add to Firestore 'listings' collection (see 'firestore.py')   
5. Repeat from step 3 with rentals = True (append '/rentals' to URL)
6. Update zip code in Firestore with 'scraped' = True
7. Repeat from step 1







