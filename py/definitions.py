import requests
import re
import string
from bs4 import BeautifulSoup

protocol = 'https'
dict_url_base = protocol + '://vocabulary.com'
slang_url_base = protocol + '://urbandictionary.com'
wiki_url_base = protocol + '://wiktionary.org'

printable = set(string.printable)

class Definition:
	def __init__(self, part_of_speech, definition, examples):
		self.part_of_speech = part_of_speech
		self.definition = definition
		self.examples = examples
	
	def prettify(self):
		s = self.part_of_speech + ' : ' + self.definition
		if self.examples:
			s += '\n\texamples:'
			for ex in self.examples:
				s += '\n\t"'
				s += ex.replace('\n', '\n\t')
				s += '"'
		return s

def join(result_set):
	res = ''
	for item in result_set:
		res += item
	return res

def find_slang_def(word):
	html_response = requests.get(slang_url_base + '/define.php?term=' + word, 
		headers={
			'responseType': 'document'
		}).text
		
	web_page = BeautifulSoup(html_response, 'lxml')
	if not web_page.find('body'):
		return []
		
	def_divs = web_page.find_all(class_='definition')
	
	definitions = []
	for div in def_divs:
		meaning = div.find(class_='meaning').get_text()
		meaning = ''.join(filter(lambda x: x in printable, meaning))
		
		example = div.find(class_='example')
		e = ''
		for c in example.children:
			if c.text:
				e += c.text
			elif c.name == 'br':
				e += '\n'
		e = ''.join(filter(lambda x: x in printable, e))
		
		definitions.append(Definition('slang', meaning, [e]))
		if len(definitions) == 3:
			break
	
	return definitions
	

def find_formal_def(word):
	html_response = requests.get(dict_url_base + '/dictionary/definition.ajax?search=' + word + '&lang=en', 
		headers={
			'responseType': 'document'
		}).text
		
	web_page = BeautifulSoup(html_response, 'lxml')
	word_overview = web_page.find(class_='word-area')
	if not word_overview:
		return [], None

	overviews = []
	short_overview = word_overview.find(class_='short')
	if short_overview:
		overviews.append(
			''.join(filter(lambda x: x in printable, short_overview.get_text())))
	long_overview = word_overview.find(class_='long')
	if long_overview:
		overviews.append(
			''.join(filter(lambda x: x in printable, long_overview.get_text())))

	word_definitions = web_page.find(class_='word-definitions').find('ol').find_all('li')

	first_type = None
	definitions = []
	for li in word_definitions:
		def_area = li.find(class_='definition')
		type_ = def_area.find(class_='pos-icon').get_text()
		if not first_type:
			first_type = type_
		def_ = join(def_area.findAll(text=True, recursive=False)).strip()
		def_ = ''.join(filter(lambda x: x in printable, def_))
		
		ex_area = li.find_all(class_='example')
		examples = []
		for ex in ex_area:
			examples.append(re.sub('[“”\n]', '', ex.text))
		
		definitions.append(Definition(type_, def_, examples))
	
	return overviews, definitions

def fits_criteria(el):
	return not (el.has_attr('class') and el['class'][0] in ['HQToggle', 'ib-brac', 'ib-content', 'mw-editsection', 'floatright']) and not (el.name in ['ul', 'sup', 'dl', 'br']) and el.children

def get_wiki_text(el):
	s = ''
	for child in el:
		is_tag = hasattr(child, 'has_attr')
		if not is_tag:
			s += child
		else:
			if fits_criteria(child):
				s += get_wiki_text(child)
	return s.replace('\n', '').strip()

def find_wiki_info(word):
	html_response = requests.get(wiki_url_base + '/wiki/' + word, 
		headers={
			'responseType': 'document'
		}).text
	
	web_page = BeautifulSoup(html_response, 'lxml')

	current_el = web_page.find(id='English')
	if not current_el:
		return '', []
	current_el = current_el.parent

	derivation = ''
	definitions = []
	last_title = ''
	while True:
		if not current_el:
			break
		
		if current_el.name == 'h3' or current_el.name == 'h4' or current_el.name == 'h5':
			last_title = get_wiki_text(current_el).lower()
		if current_el.name == 'ol':
			for def_ in current_el.children:
				i_text = get_wiki_text(def_)
				if not i_text:
					continue
				definitions.append(Definition(last_title, i_text, []))
		elif current_el.name == 'hr':
			break
		elif current_el.name == 'p' and last_title.startswith('etymology'):
			if derivation:
				derivation += '\n'
			derivation += get_wiki_text(current_el)

		current_el = current_el.next_sibling
	
	return derivation, definitions