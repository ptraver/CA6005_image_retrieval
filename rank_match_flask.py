
#local module
import preprocessing

#other modules
import collections, functools, operator

from json import load
from os import getcwd, listdir, remove
from os.path import exists
from sys import argv
from xml.etree.ElementTree import parse

# Load idx from json file
with open('bm25_idx_Ylabel.json') as json_file:
	idx = load(json_file)

# Take an xml topic file and return (queryid, title_list)
def parse_xml(query):
	return preprocessing.tokenize(query)

# Takes a query and returns a dictionary giving all non-zero relevance scores by collection document
def query_dot_idx(title_list2):

	idx_terms = []

	for word in title_list2:
		if word in idx:
			idx_terms.append(idx[word])

	if not idx_terms:
		return {}
	elif len(idx_terms) == 1:
		return idx_terms[0]
	else:
		return dict(functools.reduce(operator.add, map(collections.Counter, idx_terms)))

# Function for testing purposes
def display_results(resultant):
	lst = []
	for entry in sorted( ((v,k) for k,v in resultant.items()), reverse=True):
		lst.append(entry[1])
	return lst

# Takes a query and calculates relevance for all colleciton documents
def score_collection(query):
	title_list = parse_xml(query)

	title_list2 = preprocessing.preprocess(title_list)

	resultant = query_dot_idx(title_list2)

	return display_results(resultant)