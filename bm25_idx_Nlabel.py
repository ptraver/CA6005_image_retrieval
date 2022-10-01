#TIMING
from datetime import datetime
global begin_time
begin_time = datetime.now()

#local module
import preprocessing

#other modules
from collections import Counter
from json import dump, load
from math import log

	# new here
with open('text_surrogate.json') as json_file:
	txt_surrogate = load(json_file)

# BM25 hyperparameters
bm25_k = 1.2
bm25_b = 0.75

# Global variables. When complete, idx is exported for later use
idx = {}

# total number of words in the collection
global total_bag_size
total_bag_size = 0

# Export global variable idx to json
def export_idx():
	with open('BM25_idx_Nlabel.json', 'w') as fp:
		dump(idx, fp)

# Join two strings on a whitespace
def collapse(title, caption):
	#(title, caption, labels)
	try:
		return title + ' ' + caption
	except (TypeError):
		return str(title) + ' ' + str(caption)

	#try:
	#	return title + ' ' + caption + ' ' + labels
	#except (TypeError):
	#	return str(title) + ' ' + str(caption) + ' ' + str(labels)

# Take an xml collection file, return document ID and an amalaglamation of headline and article body
def parse_xml(fname):

	dict_entry = txt_surrogate[fname]

	title = dict_entry['title']
	caption = dict_entry['caption']
	#labels = dict_entry['labels']

	#txt_list = preprocessing.tokenize(collapse(title, caption, labels))
	txt_list = preprocessing.tokenize(collapse(title, caption))

	return (txt_list)

# Finds total_bag_size. Stores count of each word in each document, and document length in idx
def first_pass(fname, txt_list):

	global total_bag_size

	# length of document
	doc_len = len(txt_list)
	# update total bag size
	total_bag_size += doc_len

	# find counts of word in txt_list
	counts = Counter(txt_list)

	# store (word frequency, doc length) for each word-document pair
	for word in counts:
		if word in idx:
			idx[word][fname] = (counts[word], doc_len)
		else:
			idx[word] = {fname: (counts[word], doc_len)}

# Takes total number of documents in collection and average docuemnt length, applies BM25 forumla to all values in idx
def second_pass(docN, avg_doc_len):
	for word in idx:
		docn_w_word = len(idx[word])
		for fname in idx[word]:
			wfreq_and_doc_len = idx[word][fname]
			# Apply BM25 formula
			idx[word][fname] = log((( docN - docn_w_word + 0.5) / docn_w_word + 0.5 ) + 1)  *  wfreq_and_doc_len[0] * (bm25_k + 1)  /  ( wfreq_and_doc_len[0] + (  bm25_k * (1 - bm25_b + bm25_b * (wfreq_and_doc_len[1] / avg_doc_len))) )

# Parse an xml document, preprocess it and add it to idx
def add_doc_to_index(fname):
	txt_list = parse_xml(fname)

	txt_list2 = preprocessing.preprocess(txt_list)
	first_pass(fname, txt_list2)
	
if __name__ == "__main__":

	for filename in txt_surrogate:
		add_doc_to_index(filename)

	# Find average document length
	docN = len(txt_surrogate)
	avg_doc_len = total_bag_size / docN

	# complete the BM25 index with a second pass through idx
	second_pass(docN, avg_doc_len)

	# save idx as json
	export_idx()

	# print timing stats
	print('BM25 indexing timing: {}'.format(datetime.now() - begin_time))