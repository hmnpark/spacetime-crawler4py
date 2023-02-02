from utils.stopwords import STOPWORDS
from urllib.parse import urlparse

def _subdomain_check(parsed_url, domain = '.ics.uci.edu'):
    return parsed_url.netloc.endswith(domain) and parsed_url.netloc != 'www.ics.uci.edu'

def _get_total_words(self, frequencies: {str: int}):

        total = 0
        for _, freq in frequencies.items(): #word here doesnt matter
            total+=freq
        return freq

class Report:

    COMMON_WORD_CUTOFF = 50
    
    '''
    This report will keep track of 50 most common words as well as the longest page in terms of words
    but it will not handle the distinct urls found or the subdomain as the frontier and worker classes
    both log that information
    '''
    def __init__(self):
        self._word_frequencies = {} #this will keep track of total word frequencies 
        self._longest_page = 0 
        self._longest_page_url = None
        self._ics_subdomains = {} #this will keep track of subdomains and the pages found in the subdomain
    
    def add_page(self,url, frequencies):
        
        parsed = urlparse(url)
        if _subdomain_check(parsed): #if a url is in the domain ics, then add to the subdomains 
            self._ics_subdomains[parsed.scheme + parse.netloc] = self._ics_subdomains.get(parsed.scheme + parse.netloc, 0) + 1
            ##this increments the pages in a subdomain each time one is detected 
            ##specifically looks for pages in the ics domain
        self._update_frequencies(frequencies) ##total frequencies will be updated
        self._update_longest_page(url, frequencies) ##longest page will be updated

    def _update_frequencies(self,frequencies: {str: int}):
        
        for word, freq in frequencies.items():
            self._word_frequencies[word] = self._word_frequencies.get(word, 0) + freq
    
    def _update_longest_page(self, url, frequencies):
        page_length = self._get_total_words(frequencies)

        if page_length > self._longest_page:
            self._longest_page = page_length
            self._longest_page_url = url #url will be tracked

    def _get_most_common_words(self, n) -> list:
        sorted_freqs = sorted(self._word_frequencies.items(), key = (lambda x: (-x[1], x[0]))): #sorts by frequency and order ties by alphabteical order
        return [(word,freq) for (word,freq) in sorted_freqs[:n] if word not in stopwords.STOPWORDS] #checks to see if there are common stopwords and excludes such words

    def print_report(self):

        ##maybe get unqiue pages from the frontier - this would be a convenience thing
        print("REPORT:")
        print(f'The longest page in terms of words was {self._longest_page_url} with {self._longest_page} words.\n')
        print("The 50 most common words (ignoring English stopwords) were:")
        for w,f in self._get_most_common_words(COMMON_WORD_CUTOFF):
            print(f'{w} --> {f}')
        
        print("Subdomains in ics.uci.edu (subdomain url --> pages detected in subdomain): ")
        for sd, freq in self._ics_subdomains.items():
            print(f'{sd} --> {freq}')
        
        
        



        
        