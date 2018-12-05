import os


def get_wordlist(language, wordlist_file):
    wordlist = []

    if not language.endswith('.txt'):
        language = language + '.txt'

    infile = wordlist_file or os.path.join(
        os.path.dirname(__file__), 'wordlists', language)

    with open(infile, 'r') as f:
        for line in f:
            wordlist.append(line.strip())

    word_to_idx = {}
    for idx in range(0, len(wordlist)):
        word_to_idx[wordlist[idx]] = idx

    return (wordlist, word_to_idx)
