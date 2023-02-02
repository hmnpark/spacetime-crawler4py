# report.py

from urllib.parse import urlparse
# import tokenizer doesnt deal with html markup


class Report:
    CUTOFF = 50
    STOP_WORDS = {'a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 
    'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 
    'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 
    'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 
    'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", 
    "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 
    'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', 
    "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 
    'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours', 
    'ourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 
    'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 
    'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", 
    "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 
    'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 
    'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 
    'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", 
    "you're", "you've", 'your', 'yours', 'yourself', 'yourselves'}
    DOMAIN = ".ics.uci.edu"

    
    def __init__(self):
        self._unique_pages = 0
        self._longest_page = ("", 0)
        self._word_frequencies = {}
        self._subdomains = {}


    def report(self):
        # Prints out the analytics of the report.
        print(f'1. How many unique pages did you find?:\n{self._get_unique_pages()}\n')
        print(f'2. What is the longest page in terms of the number of words?:\n{self._get_longest_page()}\n')
        print(f'3. What are the 50 most common words in the entire set of pages crawled under these domains?:\n{self._get_common_words()}\n')
        print(f'4. How many subdomains did you find in the ics.uci.edu domain?:\n{self._get_subdomains()}')


    def add_page(self, url, resp):
        # Adds a unique page and updates others accordingly.
        parsed = urlparse(url)
        words = []
        self._unique_pages += 1
        self._update_longest_page(self, url, len(words))
        self._add_words(self, words)
        self._add_subdomain(self, parsed)


    def _update_longest_page(self, url, num):
        # Updates the longest page by comparing number of words.
        if (self._longest_page[1] < num):
            self._longest_page = (url, num)


    def _add_words(self, words):
        # Adds words in the set that are not English stop words.
        for word in words:
            if word not in Report.STOP_WORDS:
                match self._word_frequencies.get(word):
                    case None: self._word_frequencies[word] = 1
                    case _: self._word_frequencies[word] += 1


    def _add_subdomain(self, parsed):
        # Adds a subdomain found in the ics.uci.edu domain.
        if (parsed.netloc.endswith(Report.DOMAIN)):
            match self._subdomains.get(parsed.netloc):
                case None: self._subdomains[parsed.netloc] = 1
                case _: self._subdomains[parsed.netloc] += 1


    def _get_unique_pages(self) -> int:
        # Returns how many unique pages found.
        return self._unique_pages


    def _get_longest_page(self) -> str:
        # Returns the longest page in terms of the number of words.
        return self._longest_page[0]


    def _get_common_words(self) -> list[str]:
        # Returns the list of common words ordered by frequency.
        return sorted(self._word_frequencies, 
        key=lambda k: self._word_frequencies[k], 
        reverse=True)[:Report.CUTOFF]


    def _get_subdomains(self) -> list[str]:
        # Returns the list of URL, number ordered alphabetically.
        return [f'{k}, {self._subdomains[k]}' for k in sorted(self._subdomains)]
