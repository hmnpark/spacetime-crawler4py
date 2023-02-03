from utils.response import Response
from utils.content_filter import _get_total_stopwords, _get_total_words
from utils.simhash import Simhash
from utils import get_logger

from urllib.parse import urlparse

from logging import Logger

s_logger = get_logger(f"Scraper", "Scraper")


def log_simhash(
    resp: Response,
    is_similar_to: str,
    simhash: Simhash,
    logger: Logger
    ) -> None:
    '''SIMHASH <similarity> LINK1 is similar to LINK2'''
    parsed = urlparse(resp.url)
    link = parsed.netloc + parsed.path + parsed.query
    similarity = simhash.compute_similarity(link, is_similar_to)
    logger.info(f'SIMHASH <{similarity}> {resp.url} is similar to {is_similar_to}')


def log_high_txt_info_content(
    resp: Response,
    frequencies: dict[str, int],
    logger: Logger
    ) -> None:
    '''
    If there are 0 words, the ratio will be -1.
    HIGH TXT INFO %ratio% stopwords=INT, total=INT LINK
    '''
    total_stop_words = _get_total_stopwords(frequencies) 
    total_words = _get_total_words(frequencies)
    ratio = -1 if total_words == 0 else total_stop_words / total_words
    logger.info(f'HIGH TXT INFO %{ratio}% stopwords={total_stop_words}, total={total_words} {resp.url}')