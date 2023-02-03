from utils.stopwords import STOPWORDS
from urllib.parse import urlparse

Token = str #for type annotations


def _subdomain_check(parsed_url: 'urlparse.ParseResult', domain = '.ics.uci.edu') -> bool:
    return parsed_url.netloc.endswith(domain) and parsed_url.netloc != 'www.ics.uci.edu' ##if a netloc ends with the domain and is not the domain then it is a subdomain

def _get_total_words(frequencies: dict[Token: int]) -> int:

    total = 0
    for _, freq in frequencies.items(): #word here doesnt matter
        total+=freq
    return total

class Report:
    
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
    
    def add_page(self,url: str, frequencies: dict[Token: int]) -> None:
        
        '''
        Takes in a url and a frequencies dict and adds an occurence of a subdomain to the _ics_subdomains dict. Also updates the total word
        frequency dict with the frequencies passed in and updates the longest page encountered
        '''

        parsed = urlparse(url)
        if _subdomain_check(parsed): #if a url is in the domain ics, then add to the subdomains 
            self._ics_subdomains[parsed.scheme + parsed.netloc] = self._ics_subdomains.get(parsed.scheme + parsed.netloc, 0) + 1
            ##this increments the pages in a subdomain each time one is detected 
            ##specifically looks for pages in the ics domain
        self._update_frequencies(frequencies) ##total frequencies will be updated
        self._update_longest_page(url, frequencies) ##longest page will be updated

    def _update_frequencies(self,frequencies: dict[Token: int]) -> None:
        '''
        Takes in a frequencies dict and updates the total occurences of each token in the word_frequencies dict 
        '''
        for word, freq in frequencies.items():
            self._word_frequencies[word] = self._word_frequencies.get(word, 0) + freq 
    
    def _update_longest_page(self, url: str, frequencies: dict[Token:int]) -> None:

        '''
        Uses the _get_total_words helper function to count the amount of words on the page, and updates the max accordingly, storing this
        length and the relevant url.
        '''
        page_length = _get_total_words(frequencies)

        if page_length > self._longest_page:
            self._longest_page = page_length
            self._longest_page_url = url #url will be tracked

    def _get_most_common_words(self, n = 50) -> list:

        '''
        Takes in a threshold (default 50) and returns a list of the n most common words seen ordered. Ties are resolved alphabetically and stopwords are ignored
        '''
        sorted_freqs = sorted(self._word_frequencies.items(), key = (lambda x: (x[0] in STOPWORDS, -x[1], x[0])))
        #sorts by frequency and order ties by alphabteical order
        ##The lamdba function returns a true or false value for the first tuple element, and the true tuples represent 
        ##stop words, which will essentially be pushed to the end of the sort as true > false
        
        return sorted_freqs[:n] #checks to see if there are common stopwords and excludes such words

    def report(self) -> str:

        '''
        Prints a formatted report of the word frequencies, the longest page encountered and its url, the 50 most common words, and the
        subdomains in ics.uci.edu as well as the pages they link to
        '''
        ##maybe get unique pages from the frontier - this would be a convenience thing

        result = ''
        result += 'REPORT:'
        result += f'The longest page in terms of words was {self._longest_page_url} with {self._longest_page} words.\n\n'
        result += f'The 50 most common words (ignoring English stopwords) were:'
        for w,f in self._get_most_common_words():
            result += f'{w} --> {f}\n'
        
        result+="Subdomains in ics.uci.edu (subdomain url --> pages detected in subdomain):\n"
        for sd, freq in self._ics_subdomains.items():
            result+=f'{sd} --> {freq}\n'
        result+='END OF REPORT\n'
        return result
