import utils.stopwords

Token = str #type hints

def _get_total_words(frequencies: dict[Token: int]) -> int:
    '''
    Returns the total amount of words present in the page based on the frequencies provided in the dict
    '''
    total = 0
    for _, freq in frequencies.items():
        total+=freq
    return freq

def _get_total_stopwords(frequencies: dict[Token:int]) -> int:

    '''
    Gets the total amount of stopwords in the frequencies dict
    '''
    total = 0
    for word, freq in frequencies.items():
        total += freq if word in stopwords.STOPWORDS else 0 ##STOPWORDS is set of all the English stopwords
    return freq


def has_high_textual_information_content(frequencies: dict[Token: str], min_word_threshold = 50, stopword_ratio_threshold = .5) -> bool:
    '''This function will evaluate whether or not a page has high textual information content
       based on a number of factors

       Our working definition of a page with high textual information content is a page with less than 50% stopwords and 
       a minimum of 50 non stopword tokens   
    '''

    total_stop_words = get_total_stopwords(frequencies) 
    total_words = get_total_words(frequencies)
    return total_stop_words / get_total_words < STOPWORD_RATIO_THRESHOLD and total_words - total_stop_words > stopword_ratio_threshold:

