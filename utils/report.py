from utils.response import Response
from utils import get_urlhash, normalize
from utils.stopwords import STOPWORDS
from urllib.parse import urlparse
import os
import shelve

# For Type Annotations.
Token = str

WORD_FREQ_FILE = 'word_freq.shelve'
ICS_SUBDOMAINS_FILE = 'ics_subdomains.shelve'
REPORT_VARS_FILE = 'report_vars.shelve'


def _subdomain_check(parsed_url: 'urlparse.ParseResult', domain = '.ics.uci.edu') -> bool:
    return parsed_url.netloc.endswith(domain) and parsed_url.netloc != 'www.ics.uci.edu' ##if a netloc ends with the domain and is not the domain then it is a subdomain


def _get_total_words(frequencies: dict[Token: int]) -> int:
    total = 0
    for _, freq in frequencies.items(): total += freq
    return total


class Report:
    '''
    This report will keep track of 50 most common words as well as the longest page in terms of words
    but it will not handle the distinct urls found or the subdomain as the frontier and worker classes
    both log that information
    '''
    def __init__(self, restart):
        if restart and os.path.exists(WORD_FREQ_FILE):
            print('Found word frequency save file and deleting it.')
            os.remove(WORD_FREQ_FILE)
        if restart and os.path.exists(ICS_SUBDOMAINS_FILE):
            print('Found ICS subdomains save file and deleting it.')
            os.remove(ICS_SUBDOMAINS_FILE)
        if restart and os.path.exists(REPORT_VARS_FILE):
            print('Found Report vars save file and deleting it.')
            os.remove(REPORT_VARS_FILE)
        # this will keep track of total word frequencies
        self._word_frequencies = shelve.open(WORD_FREQ_FILE)  
        # this will keep track of subdomains and the pages found in the subdomain
        self._ics_subdomains = shelve.open(ICS_SUBDOMAINS_FILE) 
        # keeps track of longest page and url, and # of unique urls
        self._report_vars = shelve.open(REPORT_VARS_FILE)

        if restart:
            self._report_vars['longest_page'] = 0
            self._report_vars['longest_page_url'] = None
            self._report_vars['unique_urls'] = 0


    def add_page(self, url: str, frequencies: dict[Token: int]) -> None:
        '''
        Takes in a url and a frequencies dict and adds an occurence of a subdomain to the _ics_subdomains dict. Also updates the total word
        frequency dict with the frequencies passed in and updates the longest page encountered
        '''
        self._report_vars['unique_urls'] += 1
        parsed = urlparse(url)
        self._update_frequencies(frequencies) ##total frequencies will be updated
        self._update_longest_page(url, frequencies) ##longest page will be updated
    

    def add_to_page_count_per_ics_subdomain(self, resp: Response, valid_links: list[str], seen: dict|set) -> None:
        '''Keeps track of the number of unique pages found in each subdomain of ics.uci.edu'''
        # check that the parent page is a ics.uci.edu subdomain
        parsed = urlparse(resp.url)
        if not _subdomain_check(parsed):
            return

        # need to check links for uniqueness
        unique_links = set()
        for link in valid_links:
            if get_urlhash(normalize(link)) not in seen and link not in unique_links:
                unique_links.add(link)

        subdomain = f'{parsed.scheme}://{parsed.netloc}'
        self._ics_subdomains[subdomain] = self._ics_subdomains.get(subdomain, 0) + len(unique_links)


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

        if page_length > self._report_vars['longest_page']:
            self._report_vars['longest_page'] = page_length
            self._report_vars['longest_page_url'] = url #url will be tracked


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

        result = '\n'
        result += 'REPORT:\n'
        result+=f'Crawler encountered {self._report_vars["unique_urls"]} unique pages\n'
        result += f'The longest page in terms of words was {self._report_vars["longest_page_url"]}' \
            + f"with {self._report_vars['longest_page']} words.\n\n"
        result += f'The 50 most common words (ignoring English stopwords) were:\n'
        for w,f in self._get_most_common_words():
            result += f'{w} --> {f}\n'
        result+=f'Crawler encountered {len(self._ics_subdomains)} subdomains\n'
        result+='Subdomains in ics.uci.edu (subdomain_url, pages detected in subdomain):\n'
        for sd, freq in sorted(self._ics_subdomains.items()):
            result+=f'{sd}, {freq}\n'
        
        result+=f'Crawler encountered {len(self._ics_subdomains)} subdomains\n'
        result+='Subdomains in ics.uci.edu (subdomain_url, pages detected in subdomain):\n'
        for sd, freq in sorted(self._ics_subdomains.items()):
            result+=f'{sd}, {freq}\n'
        result+='END OF REPORT\n'
        return result
