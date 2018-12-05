from flask import Flask
from azure.cognitiveservices.search.websearch import WebSearchAPI
from azure.cognitiveservices.search.websearch.models import SafeSearch
from msrest.authentication import CognitiveServicesCredentials
import nltk
import re
import urllib
from bs4 import BeautifulSoup
import html2text

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
	subscription_key = "df77ddcd467a4c399dc8995de0422bd1"

	# instantiate the client.
	client = WebSearchAPI(CognitiveServicesCredentials(subscription_key))

	# read locations excel from berlin.de
	assure_csv_file()
	print('berlinLocations ... loaded')
	locationsBerlin  = pandas.read_excel(os.path.join(DATA_BASE_PATH, CSV_NAME))

	# interate over all locations and find corresponding opening hours
	for index, row in locationsBerlin.iterrows():

		# create bing request
		query = row['Institution'] + " visitberlin.de" #definition of the query
		searchResponse = client.web.search(query=query, setLang="GB", count=20) #execute the query on the bing web search api
		
		if hasattr(searchResponse.web_pages, 'value'):

			#iterate over all found webpages 
			for index in range(1, len(searchResponse.web_pages.value)):

				foundPage = searchResponse.web_pages.value[index]

				# => Step 1: Evaluate if current found webpage is interesting ...

				# 1a: URL contains /en/ AND visitberlin.de
				if "/en/" not in foundPage.url or "visitberlin.de" not in foundPage.url:
					continue

				# 1b: URL's last parts is (somehow) similar to the searched point of interest
				urlParts = foundPage.url.split("/") #split the url
				lastUrlPart = urlParts[-1] #get the last part of the url
				stripped_lastUrlPart = re.sub('[-!$%^&*()_+|~=`{}\[\]:\";\'<>?,.\/\d]', ' ', lastUrlPart) #get rid of special symbols
				
				jd = nltk.jaccard_distance(set(stripped_lastUrlPart.lower()), set(row['Institution'].lower())) #calculate the similarity

				# - Documentation -
				# The threshold of 0.52 was created by a manual evaluation of the following output:
				# print( str(lastUrlPart)+"|"+str(stripped_lastUrlPart)+"|"+str(row['Institution'])+"|"+str(1-jd) )

				if 1-jd < 0.52: 
					continue #stop the evaluation of the current webpage if similarity is below a certain threshold

				# => From here on: The webpage is regarded as a matching webpage

				# - Debugging -
				# print(str(index)+". web page name: {} ".format(foundPage.name))
				# print(str(index)+". web page URL: {} ".format(foundPage.url))

				# => Step 2: Scrape the found webpage ...

				# 2a: Open webpage and parse it
				page = urllib.request.urlopen(foundPage.url)
				soup = BeautifulSoup(page, 'html.parser')
				
				# 2b: Find content-divs and iterate over all included p-tag elements
				contentDiv = soup.findAll('div', attrs={'class':'content'})
				
				#print("=================== DIV ===================")
				cleanedHtml = "" # resulting string
				for div in contentDiv:
					for p in div.findAll('p'):
						clean = cleanhtml(str(p.text)) #code is cleaned of links and other html tags inside the p-element
						cleanedHtml += "\r\n"+clean
						#print(clean)

				print(row['Institution']+": Webpage found and read")
				#print(cleanedHtml)

				

				break #stop for loop because a corresponding article was found

				#print(contentDiv)
				#print(range(1,len(contentDiv)))
				#if isinstance(contentDiv, int):
				#	continue

				#print(cleanhtml(str(contentDiv[1])))

				#print("laenge:"+str(len(contentDiv)))
				#if(contentDiv == null)
				#for div in range(1, len(contentDiv)):
				#	cleantext = cleanhtml(str(contentDiv[div]))
				#	#cleantext = BeautifulSoup(contentDiv[div], "lxml").text
				#	print(cleantext)

				# initialize html code cleaner
				#h = html2text.HTML2Text()
				#h.ignore_links = True
				#h.escape_all = True

				# do the html code cleaning
				
				#for div in range(1, len(contentDiv)):
				#	try:
				#		p
				#		cleanedHtml = str(cleanhtml(div)) #str(h.handle(div))
				#	except:
				#		cleanedHtml = cleanedHtml
				#print("HTML (cleaned): "+cleanedHtml)
				#print(str(len(contentDiv)))

		else:
			print(row['Institution']+": No webpage")


		#locationsBerlin.loc[index,'website'] = str(placeDetails['website'])	
        
	#writer = pandas.ExcelWriter('output.xlsx')
	#locationsBerlin.to_excel(writer,'Sheet1')
	#writer.save()

	return ""

def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext


@app.route('/test')
def test():

	# setup connection to google places api

	return ""
