from collections import defaultdict
from utils.response import Response
import re


Token = str # for type hints


def computeWordFrequencies(text_from_html: str) -> defaultdict[Token, int]:
    '''
    Takes in a string, splitting on any non-alphanumeric chars.
    Returns a mapping of the tokens to their frequency.
    '''
    frequencies = defaultdict(int)
    tokens = _tokenize(text_from_html)

    for token in tokens:
        frequencies[token] += 1
    return frequencies


def _tokenize(to_be_tokenized: str) -> list[Token]:
    '''Tokenizes a string by splitting on any non-alphanumeric char.'''
    tokens = list()
    # while loop runs until EOF
    for line in to_be_tokenized.split('\n'):
        # tokenize file line by line
        _tokenize_line(line, tokens)
    return tokens

def _tokenize_line(line: str, tokens: list[Token]) -> None:
    '''Tokenizes a line. Helper for _tokenize.'''
    pattern = r'[^a-zA-Z0-9]'   # matches any non-alphanumeric char
    for token in re.split(pattern, line):   # split on non-alphanumeric chars
        if _is_valid_token(token):
            tokens.append(token.lower())

def _is_valid_token(token: str) -> bool:
    '''Checks if the token is valid.'''
    # checks that string is alphanumeric
    return token.isalnum()
