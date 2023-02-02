import utils.stopwords
class Report:

    COMMON_WORD_CUTOFF = 50

    def __init__(self):
        self._word_frequencies = {}
        self._longest_page = 0
        self._unique_urls = set()
        self._longest_page_url = None
    
    def add_page(url, frequencies):

        self._update_frequencies(frequencies)
        self._update_longest_page(url, frequencies)

    def _update_frequencies(frequencies: {str: int}):
        
        for word, freq in frequencies.items():
            self._word_frequencies[word] = self._word_frequencies.get(word, 0) + freq
    
    def _get_total_words (frequencies: {str: int}):

        total = 0
        for _, freq in frequencies.items():
            total+=freq
        return freq
    
    def _update_longest_page(url, frequencies):
        page_length = self._get_total_words(frequencies)

        if page_length > self._longest_page:
            self._longest_page = page_length
            self._longest_page_url = url

    def _get_most_common_words(n) -> list:
        sorted_freqs = sorted(frequencies.items(), key = (lambda x: (-x[1], x[0]))): 
        return [word for word in sorted_freqs[:n] if word not in stopwords.STOPWORDS]

    def print_report():
        pass
        

        



