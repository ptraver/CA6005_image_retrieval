
import datetime
begin_time = datetime.datetime.now()

from bs4 import BeautifulSoup
from json import dump
import os
import requests
import wikipedia as wp

headers = {'User-Agent': 'My User Agent 1.0'}

years = ['2010', '2011', '2012', '2013', '2014']
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']

#years = ['2004']
#months = ['May']


output_dict = {}


def getdata(url): 
    r = requests.get(url, headers=headers, stream=True)
    return r.text 


# Get html page

for year in years:
	for month in months:

		htmldata = getdata(f"https://en.wikipedia.org/wiki/Wikipedia:Picture_of_the_day/{month}_{year}")
		soup = BeautifulSoup(htmldata, 'html.parser')

		# Unique identifier image

		query = f"Wikipedia:Picture of the day/{month} {year}"
		wp_page = wp.page(query)
		list_img_urls = wp_page.images

		imgs = soup.find_all('a', class_='image')

		# Use the image url to download it
		# This is made much simpler with wikipedia api

		successes = []

		for img in list_img_urls:

			#href = img['href']

			#url = 'https:' + img.get('src')

			response = requests.get(img, headers=headers, stream=True)	#my_session.get(url, timeout=100)

			if response.status_code == 200:
				filename = img.split("/")[-1]

				file = open(os.getcwd() + '/imgs/' + filename, 'wb')
				file.write(response.content)
				file.close()

				successes.append(filename)
				print(f'downloaded {month} {year} {filename}')
			else:
				print(f'{month} {year} {filename} could not be retrieved')

		for img in imgs:
			filename = img['href'].split(':')[-1]
			if filename in successes:
				
				td = img.parent
				p = td.findNext('p')

				supp_p = p.findNext('p')
				supp_p_ch = supp_p.findChildren('small', recursive=False)

				if not supp_p_ch:
					caption = p.get_text().rstrip() + ' ' + supp_p.get_text().rstrip()
				else:
					caption = p.get_text().rstrip()

				if img.has_attr('title'):
					output_dict[filename] = {'title': img['title'], 'caption': caption}
				else:
					output_dict[filename] = {'title': '', 'caption': caption}

				print(f'saved textual surrogate for {month} {year} {filename}')

with open('text_surrogate.json', 'w') as fp:
	dump(output_dict, fp)

# 25 mins .. quicker this time..??
print(f'time to save 5 years of wiki pic of day images w text surrogates: {datetime.datetime.now() - begin_time}')

		#with open('text_surrogate.json') as json_file:
		#	dct = load(json_file)

				#print(supp_p_ch)
				#print(td)

				#print(img['title'])



				#print(soup.find(text=filename).findNext('p').contents)