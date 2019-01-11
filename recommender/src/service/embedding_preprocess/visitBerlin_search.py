from azure.cognitiveservices.search.websearch import WebSearchAPI
from azure.cognitiveservices.search.websearch.models import SafeSearch
from msrest.authentication import CognitiveServicesCredentials
import re
import urllib
from bs4 import BeautifulSoup
import html2text
from src.service.persistency.persistence_service import get_all_points_of_interests

from py_stringmatching import SmithWaterman

#from .persistence_service import get_all_points_of_interests

# -------- code from sebastian ---------
from urllib.request import urlretrieve
import os
import pandas

class VisitBerlin:

	DATA_BASE_PATH = 'data/'
	CSV_NAME = 'open_data_berlin_cultural_institutes.xlsx'
	CSV_URL = 'http://www.berlin.de/sen/kultur/_assets/statistiken/kultureinrichtungen_alle.xlsx'

	def __init__(self):
		self.data = self.initializeArticles()
		print("stopper")

	def assure_csv_file(self):
		if not os.path.exists('data'):
			os.makedirs('data')

		if not os.path.exists(self.DATA_BASE_PATH + self.CSV_NAME):
			print('downloading CSV file...')
			response = urlretrieve(self.CSV_URL, self.DATA_BASE_PATH + self.CSV_NAME)

	def perform_acqusition(self):
		self.assure_csv_file()

		data_frame = pandas.read_excel(os.path.join(self.DATA_BASE_PATH, self.CSV_NAME))

		for index, row in data_frame.iterrows():
			row['Institution']
			row['Adresse']
			row['Lat']
			row['Lon']
	# -------- END: code sebastian ---------


	def initializeArticles(self):

		# subscription key for Bing, needs to be renewed regularly
		subscription_key = "8539f7d32c9d40848fcb61bd34febfb5"

		# instantiate the client.
		client = WebSearchAPI(CognitiveServicesCredentials(subscription_key))

		# read locations excel from berlin.de
		self.assure_csv_file()
		print('berlinLocations ... loaded')
		locationsBerlin  = pandas.read_excel(os.path.join(self.DATA_BASE_PATH, self.CSV_NAME))

		# initialize dataframe for method's result
		resultingDataFrame = pandas.DataFrame(index=range(0, len(locationsBerlin)-1), columns=['id','institution','textFromVisitBerlin'])
		resultingDataFrame.fillna(0) 

		# interate over all locations and find corresponding opening hours
		for locationIndex, row in locationsBerlin.iterrows():

			# create bing request
			query = row['Institution'] + " site:visitberlin.de/en" #definition of the query
			searchResponse = client.web.search(query=query, setLang="GB", count=20) #execute the query on the bing web search api

			# write location name into result dataframe
			resultingDataFrame.loc[locationIndex,'institution'] = row['Institution'] 
			
			if hasattr(searchResponse.web_pages, 'value'):

				validWebpageFound = False

				#iterate over all found webpages 
				for searchResultIndex in range(0, len(searchResponse.web_pages.value)):

					foundPage = searchResponse.web_pages.value[searchResultIndex]

					# => Step 1: Evaluate if current found webpage is interesting ...
					# URL's last parts is (somehow) similar to the searched point of interest
					urlParts = foundPage.url.split("/") #split the url
					lastUrlPart = urlParts[-1] #get the last part of the url

					# remove other request parameters
					if lastUrlPart.find('?') != -1:
						lastUrlPart = lastUrlPart[0:lastUrlPart.find('?')]
					
					stripped_lastUrlPart = re.sub(r'[-!$%^&*()_+|~=`{}\[\]:\";\'<>?,.\/\d]', ' ', lastUrlPart) #get rid of special symbols

					# normalized smith waterman score
					sw = SmithWaterman()
					sim = sw.get_raw_score(stripped_lastUrlPart.lower(), row['Institution'].lower()) / max(len(stripped_lastUrlPart), len(row['Institution']))

					# - Debugging -
					# print(sim)
					# print(stripped_lastUrlPart.lower(), '\n', row['Institution'].lower())
					# print(str(searchResultIndex)+". web page name: {} ".format(foundPage.name))
					# print(str(searchResultIndex)+". web page URL: {} ".format(foundPage.url))

					if sim < 0.5 and foundPage.name.find(row['Institution']) == -1: 
						continue #stop the evaluation of the current webpage if similarity is below a certain threshold

					# => From here on: The webpage is regarded as a matching webpage

					# => Step 2: Scrape the found webpage ...

					# 2a: Open webpage and parse it
					page = urllib.request.urlopen(foundPage.url)
					soup = BeautifulSoup(page, 'html.parser')
					
					# 2b: Find content-divs and iterate over all included p-tag elements
					contentDiv = soup.findAll('div', attrs={'class':'content'})
					
					cleanedHtml = "" # resulting string
					for div in contentDiv:
						for p in div.findAll('p'):
							validWebpageFound = True #page was found else not
							clean = self.cleanhtml(str(p.text)) #code is cleaned of links and other html tags inside the p-element
							cleanedHtml += "\r\n"+clean
							#print(clean)

					# write text from visitBerlin into result dataframe
					resultingDataFrame.loc[locationIndex,'textFromVisitBerlin'] = cleanedHtml 


					print("{}: {}".format(row['Institution'], foundPage.url))


					break #stop for loop because a corresponding article was found

			# if content div was not found
			if not validWebpageFound:
				print(row['Institution']+": No webpage")

			#locationsBerlin.loc[locationIndex,'website'] = str(placeDetails['website'])	
			
		#writer = pandas.ExcelWriter('output.xlsx')
		#locationsBerlin.to_excel(writer,'Sheet1')
		#writer.save()

		return resultingDataFrame

	def cleanhtml(self, raw_html):
		cleanr = re.compile('<.*?>')
		cleantext = re.sub(cleanr, '', raw_html)
		return cleantext

	def find(self, name):
		for locationIndex in range(0, len(self.data)):
			if self.data.loc[locationIndex, 'institution'] == name:
				return self.data.loc[locationIndex, 'textFromVisitBerlin']
		return None

	def perform_visitBerlin_lookup(self):
		columns = ['id', 'name', 'street_name', 'street_number', 'zip_code', 'long', 'lat', 'opening_hours', 'word2vec']
		dataframe = pandas.DataFrame(get_all_points_of_interests(), columns = columns)[['id', 'name']]

		dataframe['text'] = dataframe.apply(lambda row: self.find(row['name']), axis = 1)

		return dataframe
