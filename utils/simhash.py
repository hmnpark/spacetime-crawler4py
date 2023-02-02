from utils.response import Response
from urllib.parse import urlparse


NUM_BITS = 64


class Simhash():
    _fingerprints: dict[str, int]
    _threshold: float

    def __init__(self, threshold=0.9) -> None:
        self._fingerprints = dict()
        self._threshold = threshold

    def is_similar(self, resp: Response, freqs: dict[str, int]) -> str:
        '''Return the url with similar content if found, else None.'''
        # use url minus fragment as key to store fingerprint
        parsed = urlparse(resp.url)
        url = parsed.netloc + parsed.path + parsed.query
        if url not in self._fingerprints:
            self._add_fingerprint(url, freqs)

        # compare the fingerprint to all others
        for other_url in self._fingerprints:
            if url != other_url and self._are_near(url, other_url):
                return other_url
        return None
    
    def compute_similarity(self, url_a: str, url_b: str) -> float:
        '''
        Return the similarity value of the url's,
        or 0 if either have not previously been compared.
        '''
        if url_a not in self._fingerprints or url_b not in self._fingerprints:
            return 0

        fingerprint_a = self._fingerprints[url_a]
        fingerprint_b = self._fingerprints[url_b]
        # get intersection of the bits of fingerprints
        intersect_bits = ~(fingerprint_a ^ fingerprint_b)

        # sum up bits
        count_bits = 0
        for _ in range(NUM_BITS):
            count_bits += 1 if 1 & intersect_bits else 0
            intersect_bits >>= 1

        return count_bits / NUM_BITS

    def _are_near(self, url_a: str, url_b: str) -> bool:
        '''Returns true if fingerprint_a and fingerprint_b are near duplicates.'''
        return self.compute_similarity(url_a, url_b) >= self._threshold

    def _add_fingerprint(self, url: str, freqs: dict[str, int]) -> None:
        '''Computes and adds fingerprint to remember.'''
        self._fingerprints[url] = self._compute_fingerprint(freqs)
        
    def _compute_fingerprint(self, freqs: dict[str, int]) -> int:
        '''Simhash algorithm. Weights determined by word frequencies.'''
        int_vector = [0] * NUM_BITS
        for token, freq in freqs.items():
            # add the current token's weight to the vector
            hash_val = hash(token)
            bin_str = bin(hash_val)[2:]
            for i, bit in enumerate(reversed(bin_str)):
                weight = freq if bit == '1' else -freq
                int_vector[NUM_BITS-1-i] += weight
        
        # convert the vector with sum of weights to a binary fingerprint
        fingerprint_vector = ['1' if val > 0 else '0' for val in int_vector]
        return int(''.join(fingerprint_vector), 2)
