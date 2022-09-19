import dictionary, sys

if __name__ == '__main__':
	if len(sys.argv) > 1:
		w = ' '.join(sys.argv[1:])
		word = dictionary.find_word(w)
		if not word:
			print('Could not find any definitions for \''+w+'\'')
		else:
			print(word.prettify())