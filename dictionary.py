import string
import definitions, images

printable = set(string.printable)
	
class Word:
	def __init__(self, word, overview, definitions, origin, imgs):
		self.word = word
		self.overview = overview
		self.definitions = definitions
		self.origin = origin
		self.imgs = imgs
		
	def prettify(self):
		s = 'Defintion of ' + self.word
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
		if self.imgs:
			for img in self.imgs:
				s += '\n'
				s += img
		return s


def find_word(word):
	overview, defs = definitions.find_formal_def(word)
	if not defs:
		overview = ['This word is slang and these definitions have been written by people who may not know what the word means.']
		defs = definitions.find_slang_def(word)
	origin = definitions.find_word_origin(word)
	imgs = []
	if len(defs) > 0 and (defs[0].part_of_speech == 'noun' or defs[0].part_of_speech == 'verb'):
		imgs = images.find_images(word)
	return Word(
		word,
		overview,
		defs,
		origin,
		imgs
	)

def web_page(w):
	word = find_word(w)
	s  = '<html>'
	s += '<body>'
	s += '<h1>'+word.word.capitalize()+'</h1>'
	if word.overview:
		s += '<h2>'+word.overview+'</h2>'
		for line in word.overview[1:]:
			s += '<h3>'+line+'</h3>'
	s += '</body>'
	s += '</html>'