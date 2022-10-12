import requests
from bs4 import BeautifulSoup

protocol = 'https'
stock_url_base = protocol + '://stock.adobe.com'
google_url_base = protocol + '://google.com'

def find_stock(word):
	html_response = requests.get(stock_url_base + '/search?k='+word,
		headers={
			'responseType': 'document'
		}).text
		
	web_page = BeautifulSoup(html_response, 'lxml')
	img_divs = web_page.find_all(class_='search-result-cell')
	
	imgs = []
	for div in img_divs:
		imgs.append(div.find('img')['src'])
		if len(imgs) == 3:
			break
	
	return imgs

def find_images(word):
	return [find_stock(word)]
