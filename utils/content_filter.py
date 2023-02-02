import utils.stopwords


def get_total_words(frequencies: {str: int}):
    total = 0
    for _, freq in frequencies.items():
        total+=freq
    return freq

def get_total_stopwords(frequencies):
    total = 0
    for word, freq in frequencies.items():
        total += freq if word in stopwords.STOPWORDS else 0
    return freq


def has_high_textual_information_content(frequencies, min_word_threshold = 50, stopword_ratio_threshold = .5) -> bool:
    '''This function will evaluate whether or not a page has high textual information content
       based on a number of factors'''

    total_stop_words = get_total_stopwords(frequencies)
    total_words = get_total_words(frequencies)
    return total_stop_words / get_total_words < STOPWORD_RATIO_THRESHOLD and total_words - total_stop_words > stopword_ratio_threshold:

