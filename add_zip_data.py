# Setup:
import pandas as pd
from google.cloud import firestore
import os

# Set env variable with path to credentials
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "firestore-credentials.json"
db = firestore.Client(project='webscraper-329918')

# Read csv
zips_income = pd.read_csv("2019MeanHouseholdIncome.csv")

# Convert to string
zips_income['Zipcode'] = zips_income['Zipcode'].apply(str)

# Pad zip codes with leading 0's
zips_income['Zipcode'] = zips_income['Zipcode'].apply(lambda x: f"00{x}" if len(x) == 3 else f"0{x}" if len(x) == 4 else x)

# Checks if zip code from CSV already exists in firestore database
for index, row in zips_income.iterrows():
    result = db.collection('zipcodes').document(row['Zipcode']).get()
   
   # If zip code exists in database, add income data from CSV
    if result.exists:
        #print(result.to_dict())
        zips_ref = db.collection('zipcodes').document(row['Zipcode'])
        zips_ref.set({u'2019MeanHouseholdIncome(month)': row['2019MonthlyMeanIncome']}, merge=True)





