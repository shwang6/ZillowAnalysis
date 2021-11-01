
import collections

def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        #new_key = parent_key + sep + k if parent_key else k #original
        new_key = k #this is better for this application
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


"""
Input: the search results list; should be 40 listings per list (assuming full capacity), each
entry to the list is a dictionary for each listing. Ideally this will be the output of parseSearchPage.

This function does:
	1. Flattens the nested dictionary to one layer
	2. Converts the post date and date sold from milliseconds to seconds
	3. Removes redundant variables 'beds', 'baths','addressCity','addressState', 'addressStreet', 'addressZipcode', 'countryCurrency', 'daysOnZillow', 'text', and 'zpid'
	4. Removes links to images where there is no image
Returns: a cleaned list of listings
"""

def clean_results(listings):
	assert type(listings) == list, "Object must be a list"
	assert type(listings[0]) == dict, "All entries in list must be a dictionary"
	
	redundants = ['beds', 'baths','addressCity','addressState', 'addressStreet', 'addressZipcode', 'countryCurrency', 'daysOnZillow', 'text', 'zpid']
	for i in range(len(listings)):
		if 'zpid' in listings[i].keys(): #If the listing has not already been cleaned
			#Flatten to one layer:
			listings[i] = flatten(listings[i], parent_key=False)
			#Calculate new variables
			listings[i]['postDate'] = listings[i]['timeOnZillow']/1000 #divide by 1000 because time is measured in milliseconds
			del listings[i]['timeOnZillow']
			#New result is in seconds
			#Convert this one from milliseconds to seconds:
			if 'dateSold' in listings[i].keys(): #Not all listings have a date sold
				listings[i]['dateSold'] = listings[i]['dateSold']/1000 #divide by 1000 because time is measured in milliseconds
			#Remove redundant variables
			for var in redundants:
				del listings[i][var]
				#Image variables where there are none
			for key, val in listings[i].copy().items():
				if 'https://www.zillowstatic.com/static/images/nophoto' in str(val):
					del listings[i][key]
	return listings
