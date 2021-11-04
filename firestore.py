
#Setup:
from google.cloud import firestore
import os

#Set environment variable with path to credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "firestore-credentials.json"
db = firestore.Client(project='webscraper-329918') #webscraper-329918 is the gcp project name

#***************************#
#        Retrieve Data      #
#***************************#
"""
This example retrieves all zip codes where the city is Knoxville, TN.
The data exists in the 'zipcodes' collection.
"""
zips_ref = db.collection(u'zipcodes').where('City', '==', 'KNOXVILLE').where("State", "==", "TN")
docs = zips_ref.stream()
for doc in docs:
    doc.to_dict()['Zipcode']
"""
In practice we'll use this with the condition where('Scraped', '==', False), which is how we will
keep track of which zip codes the function will scrape next.
We may want to prioritize more local zip codes first.
"""
    

#***************************#
#        Input Data         #
#***************************#
for i in range(len(all_listings)):
	doc_ref = db.collection('listings').document(all_listings[i]['id']) #Set the listing id as the document name
	doc_ref.set( all_listings[i] )
"""
This creates a new entry in the 'listings' collection that uses zillow's id number as the identifier of the listing.
If the entry exists, it will be overwritten with the new data.
'all_listings' is a list of dictionaries, each entry of the list corresponding to a listing from the search results.
"""
