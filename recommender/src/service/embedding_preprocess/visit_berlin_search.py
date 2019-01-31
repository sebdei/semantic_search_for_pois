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

from config import *

# instantiate the client.
client = WebSearchAPI(CognitiveServicesCredentials(bing_subscription_key))

def clean_html(raw_html):
	cleanr = re.compile('<.*?>')
	cleantext = re.sub(cleanr, '', raw_html)
	return cleantext

def execute_visitberlin_query(search_term):
	# create bing request
	query = search_term + " site:visitberlin.de/en" #definition of the query
	search_response = client.web.search(query=query, setLang="GB", count=20) #execute the query on the bing web search api

	valid_webpage_found = False

	if hasattr(search_response.web_pages, 'value'):


		#iterate over all found webpages
		for search_result_index in range(0, len(search_response.web_pages.value)):

			found_page = search_response.web_pages.value[search_result_index]

			# => Step 1: Evaluate if current found webpage is interesting ...
			# URL's last parts is (somehow) similar to the searched point of interest
			urlParts = found_page.url.split("/") #split the url
			lastUrlPart = urlParts[-1] #get the last part of the url

			# remove other request parameters
			if lastUrlPart.find('?') != -1:
				lastUrlPart = lastUrlPart[0:lastUrlPart.find('?')]

			stripped_last_url_part = re.sub(r'[-!$%^&*()_+|~=`{}\[\]:\";\'<>?,.\/\d]', ' ', lastUrlPart) #get rid of special symbols

			# normalized smith waterman score
			sw = SmithWaterman()
			sim = sw.get_raw_score(stripped_last_url_part.lower(), search_term.lower()) / max(len(stripped_last_url_part), len(search_term))

			# - Debugging -
			# print(sim)
			# print(stripped_last_url_part.lower(), '\n', search_term.lower())
			# print(str(search_result_index)+". web page name: {} ".format(found_page.name))
			# print(str(search_result_index)+". web page URL: {} ".format(found_page.url))

			if sim < 0.5 and found_page.name.find(search_term) == -1:
				continue #stop the evaluation of the current webpage if similarity is below a certain threshold

			# => Step 2: The webpage is regarded as a matching webpage
			# Scrape the found webpage ...

			# 2a: Open webpage and parse it
			page = urllib.request.urlopen(found_page.url)
			soup = BeautifulSoup(page, 'html.parser')

			# 2b: Find content-divs and iterate over all included p-tag elements
			contentDiv = soup.findAll('div', attrs={'class':'content'})

			cleaned_html = "" # resulting string
			for div in contentDiv:
				for p in div.findAll('p'):
					valid_webpage_found = True # page was found else not
					clean = clean_html(str(p.text)) # code is cleaned of links and other html tags inside the p-element
					cleaned_html += "\r\n"+clean
					# print(clean)

			print("{}: {}".format(search_term, found_page.url))

			return found_page.name, found_page.url, cleaned_html

	# if content div was not found
	if not valid_webpage_found:
		print(search_term+": No webpage")

		return None, None, None
