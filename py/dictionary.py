import string
import definitions, images
import urllib.parse

printable = set(string.printable)
	
class Word:
	def __init__(self, word, overview, definitions, origin, imgs, source):
		self.word = word
		self.overview = overview
		self.definitions = definitions
		self.origin = origin
		self.imgs = imgs
		self.source = source
		
	def prettify(self):
		s = 'Definition of ' + self.word
		s += '\n\n'
		for line in self.overview:
			s += line
			s += '\n\n'
		defs_len = len(self.definitions)
		s += str(defs_len) + ' definition' + ('s' if defs_len > 1 else '')
		s += '\n\n'
		for def_ in self.definitions:
			s += def_.prettify()
			s += '\n'
		if self.origin:
			s += '\n'
			s += self.origin
			s += '\n'
		if self.imgs:
			for row in self.imgs:
				for img in row:
					s += '\n'
					s += img
		return s


def find_word(word):
	overview, defs = definitions.find_formal_def(word)
	source = '<a href="https://vocabulary.com">Vocabulary.com</a>'
	origin, defs_wiki = definitions.find_wiki_info(word)
	if not defs:
		defs = defs_wiki
		source = '<a href="https://wiktionary.org">Wiktionary</a>'
		if not defs:
			overview = ['These are publicly-made definitions.',
				'These definitions may or may not be correct.']
			defs = definitions.find_slang_def(word)
			source = '<a href="https://urbandictionary.com">Urban Dictionary</a>'
			if not defs:
				overview = []
				source = None
	imgs = []
	if len(defs) > 0 and (defs[0].part_of_speech == 'noun' or defs[0].part_of_speech == 'verb'):
		imgs = images.find_images(word)
	return Word(
		word,
		overview,
		defs,
		origin,
		imgs,
		source
	)

def web_page(raw_word):
	looked_up = urllib.parse.unquote_plus(raw_word)
	word = find_word(looked_up)
	s  = '<html>'
	s += '<head>'
	s += '<title>'
	s += looked_up
	s += ' | The Everything Dictionary'
	s += '</title>'
	s += '<link rel="stylesheet" href="/style.css">'
	s += '<script src="/script.js" defer></script>'
	s += '</head>'
	s += '<body>'
	s += '<a href="/">'
	s += '<img class="logo" src="/logo_small.png" style="height: 4em; position: absolute; top: 1em;">'
	s += '</a>'
	s += '<input style="margin-top: 1.5em; margin-bottom: 2em;" type="text" placeholder="Learn a new word" id="search" onkeydown="search(this)"/>'
	s += '<div id="word">'
	s += '<h1 id="title">'+looked_up+'</h1>'
	if word.overview:
		s += '<div id="wordOverview">'
		s += '<h3>'+word.overview[0]+'</h3>'
		for line in word.overview[1:]:
			s += '<h4>'+line+'</h4>'
		s += '</div>'
	s += '<ul class="definitions">'  # definitions
	for def_ in word.definitions:
		s += '<li>'
		s += '<div class="defContent">'
		s += '<span class="part_of_speech '
		s += def_.part_of_speech
		s += '">'
		s += def_.part_of_speech
		s += '</span>'
		s += '<span class="definition"> '
		s += def_.definition.replace('\n', '<br>')
		s += '</span>'
		s += '</div>'
		if def_.examples:
			s += '<ul class="examples">'
			for ex in def_.examples:
				s += '<li class="example">'
				s += '"' + ex.replace('\n', '<br>') + '"'
				s += '</li>'
			s += '</ul>'
		s += '</li>'
	s += '</ul>'
	s += '<p id="derivation">'
	if word.origin:
		s += word.origin.replace('\n', '<br><br>')
	else:
		s += 'couldn\'t find a derivation for this word'
	s += '</p>'
	if word.imgs:
		for source in word.imgs:
			s += '<div class="img-container">'
			for img in source:
				s += '<img class="mass" src="'
				s += img
				s += '"/>'
			s += '</div>'
			s += '<p style="text-align: center;">Images from <a href="https://stock.adobe.com">Adobe Stock</a></p>'
	if word.source:
		s += '<p style="text-align: center;">Definitions from '
		s += word.source
		s += '</p>'
	if word.origin:
		s += '<p style="text-align: center;">Derivations from <a href="https://wiktionary.org">Wiktionary</a></p>'
	s += '</div>'
	s += '</body>'
	s += '</html>'
	return s
