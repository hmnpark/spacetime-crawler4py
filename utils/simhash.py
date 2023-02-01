from utils.response import Response
from urllib.parse import urlparse


class Simhash():
    _simhashes: dict[str, int]
    _threshold: float

    def __init__(self, threshold=0.9) -> None:
        self._simhashes = dict()
        self._threshold = threshold

    def is_similar(self, resp: Response, freqs: dict[str, int]) -> bool:
        pass

    def _compute_simhash(freqs: dict[str, int]) -> int:
        pass