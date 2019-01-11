from azure.cognitiveservices.search.websearch import WebSearchAPI
from msrest.authentication import CognitiveServicesCredentials
import re
import urllib
from ..persistency import data_model
from bs4 import BeautifulSoup
from src.service.persistency.persistence_service import get_all_points_of_interests

from py_stringmatching import SmithWaterman

from urllib.request import urlretrieve
import os
import pandas

# subscription key for Bing, needs to be renewed regularly
subscription_key = "8539f7d32c9d40848fcb61bd34febfb5"

# instantiate the client.
client = WebSearchAPI(CognitiveServicesCredentials(subscription_key))

def cleanhtml(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext

def execute_visitberlin_query(search_term):
	# create bing request
	query = search_term + " site:visitberlin.de/en" #definition of the query
	searchResponse = client.web.search(query=query, setLang="GB", count=20) #execute the query on the bing web search api
	
	validWebpageFound = False
	
	if hasattr(searchResponse.web_pages, 'value'):


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
			sim = sw.get_raw_score(stripped_lastUrlPart.lower(), search_term.lower()) / max(len(stripped_lastUrlPart), len(search_term))

			# - Debugging -
			# print(sim)
			# print(stripped_lastUrlPart.lower(), '\n', search_term.lower())
			# print(str(searchResultIndex)+". web page name: {} ".format(foundPage.name))
			# print(str(searchResultIndex)+". web page URL: {} ".format(foundPage.url))

			if sim < 0.5 and foundPage.name.find(search_term) == -1: 
				continue #stop the evaluation of the current webpage if similarity is below a certain threshold

			# => Step 2: The webpage is regarded as a matching webpage
			# Scrape the found webpage ...

			# 2a: Open webpage and parse it
			page = urllib.request.urlopen(foundPage.url)
			soup = BeautifulSoup(page, 'html.parser')
			
			# 2b: Find content-divs and iterate over all included p-tag elements
			contentDiv = soup.findAll('div', attrs={'class':'content'})
			
			cleanedHtml = "" # resulting string
			for div in contentDiv:
				for p in div.findAll('p'):
					validWebpageFound = True # page was found else not
					clean = cleanhtml(str(p.text)) # code is cleaned of links and other html tags inside the p-element
					cleanedHtml += "\r\n"+clean
					# print(clean)

			print("{}: {}".format(search_term, foundPage.url))

			return foundPage.name, foundPage.url, cleanedHtml

	# if content div was not found
	if not validWebpageFound:
		print(search_term+": No webpage")

		return None, None, None