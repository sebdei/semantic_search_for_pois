from flask import Flask
# from bs4 import BeautifulSoup
from googleplaces import GooglePlaces, types, lang #pip install python-google-places
from pprint import pprint


# -------- code from sebastian ---------
from urllib.request import urlretrieve
import os
import pandas

DATA_BASE_PATH = 'data/'
CSV_NAME = 'open_data_berlin_cultural_institutes.xlsx'
CSV_URL = 'http://www.berlin.de/sen/kultur/_assets/statistiken/kultureinrichtungen_alle.xlsx'

def assure_csv_file():
    if not os.path.exists('data'):
        os.makedirs('data')

    if not os.path.exists(DATA_BASE_PATH + CSV_NAME):
        print('downloading CSV file...')
        response = urlretrieve(CSV_URL, DATA_BASE_PATH + CSV_NAME)

def perform_acqusition():
    assure_csv_file()

    data_frame = pandas.read_excel(os.path.join(DATA_BASE_PATH, CSV_NAME))

    for index, row in data_frame.iterrows():
        row['Institution']
        row['Adresse']
        row['Lat']
        row['Lon']
# -------- END: code sebastian ---------


app = Flask(__name__)

@app.route('/')
def main():

	# setup connection to google places api
	API_KEY = 'AIzaSyD3NQ8gNgpYzpLfZ5M5BLCBWXg1a3_d5Zg'
	google_places = GooglePlaces(API_KEY)

	# read locations excel from berlin.de
	assure_csv_file()
	print('test')
	locationsBerlin  = pandas.read_excel(os.path.join(DATA_BASE_PATH, CSV_NAME))

	# interate over all locations and find corresponding opening hours
	for index, row in locationsBerlin.iterrows():
		#if index < 50:
		#	continue
		
		placeDetails = getSearchPacesNearBy(google_places, row['Institution']+" "+row['Adresse'])
		
		try:
			locationsBerlin.loc[index,'place_id'] = str(placeDetails['place_id'])
			print(str(placeDetails['place_id']))
		except:
			locationsBerlin.loc[index,'place_id'] = "-"	
			print("-")
		
		try:
			locationsBerlin.loc[index,'opening_hours'] = str(placeDetails['opening_hours'])
		except:
			locationsBerlin.loc[index,'opening_hours'] = "-"

		try:
			locationsBerlin.loc[index,'website'] = str(placeDetails['website'])
		except:
			locationsBerlin.loc[index,'website'] = "-"
		#locationsBerlin.loc[index,'googleapiDetails'] = str(placeDetails['opening_hours'])
		#if index > 5:
		#pprint(locationsBerlin)
		#	break

        
	writer = pandas.ExcelWriter('output.xlsx')
	locationsBerlin.to_excel(writer,'Sheet1')
	writer.save()

	return ""


@app.route('/test')
def test():

	# setup connection to google places api
	API_KEY = 'AIzaSyD3NQ8gNgpYzpLfZ5M5BLCBWXg1a3_d5Zg'
	google_places = GooglePlaces(API_KEY)

	return str(getSearchPacesNearBy(google_places, 'Berliner Ensemble'))#'Parkaue 29,10367 Berlin'))

def getSearchPacesNearBy(google_places, keyword):

	query_result = google_places.text_search(
		location='Berlin', query=keyword)

	for place in query_result.places:
		details = getPlaceDetails(google_places, place.place_id)
		return(details)

	return str(query_result.raw_response)

#	input_html = "./listAccidents.htm"
#	with open(input_html, "r") as ifile:
#		soup = BeautifulSoup(ifile, 'lxml') 
#	return soup.title.string

#    return 'Hello, World!'

def getPlaceDetails(google_places, _placeId):
	query_result = google_places.get_place(place_id=_placeId)
	return query_result.details