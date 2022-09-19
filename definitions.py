import requests, re
from bs4 import BeautifulSoup

protocol = 'https'
dict_url_base = protocol + '://vocabulary.com'
slang_url_base = protocol + '://urbandictionary.com'
deriv_url_base = protocol + '://wiktionary.org'

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
		slang_defs = find_slang_def(word)
		if not slang_defs:
			return [], None
		return Word(
			word,
			['This word is slang. Definitions may be innacurate.', 'All these definitions were pulled from people who may not know the true meaning of the word.'],
			slang_defs,
			find_word_origin(word),
			[]
		)

	word_definitions = web_page.find(class_='word-definitions').find('ol').find_all('li')

	first_type = None
	definitions = []
	for li in word_definitions:
		def_area = li.find(class_='definition')
		type_ = def_area.find(class_='pos-icon').get_text()
		if not first_type:
			first_type = type_
		def_ = join(def_area.findAll(text=True, recursive=False)).strip()
		
		ex_area = li.find_all(class_='example')
		examples = []
		for ex in ex_area:
			examples.append(re.sub('[“”\n]', '', ex.text))
		
		definitions.append(Definition(type_, def_, examples))
	
	return [
		word_overview.find(class_='short').get_text(),
		word_overview.find(class_='long').get_text()
	], definitions


def find_word_origin(word):
	html_response = requests.get(deriv_url_base + '/wiki/' + word, 
		headers={
			'responseType': 'document'
		}).text
	
	web_page = BeautifulSoup(html_response, 'lxml')
	title = web_page.find(id='Etymology')
	
	if not title:
		return ''
	
	ety = title.parent.next_sibling.next_sibling
	return ety.get_text()