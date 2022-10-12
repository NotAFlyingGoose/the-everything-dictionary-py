import dictionary, sys

if __name__ == '__main__':
	if len(sys.argv) > 1:
		w = ' '.join(sys.argv[1:])
		word = dictionary.find_word(w)
		print(word.prettify())