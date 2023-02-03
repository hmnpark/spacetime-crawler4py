import time
from logging import Logger
from urllib import urlparse

from utils.response import Response
from utils.config import Config
from utils.download import download


def robots_check(url: str, rules: dict[str, tuple[list[str], list[str]]], config: Config, logger: Logger) -> list[str]:
    '''
    If the urls authority is new, try and process the robots.txt file.
    Return the given url if it respects the rules and any new sitemap urls.
    '''
    urls = list()
    parsed = urlparse(url)
    if parsed.netloc in rules:
        # robots.txt already parsed.
        # offending urls would have been caught elsewhere.
        # can return url safely.
        return [url]

    resp = download(f'{parsed.scheme}://{parsed.netloc}/robots.txt', config, logger)
    time.sleep(config.time_delay)
    if resp != 200:
        rules[parsed.netloc] = ([], []) # no robots.txt rules to follow. allow all.
        return [url]    # no robots.txt to process
    
    urls = _process_robots(resp, rules)
    if respects_robots(url, rules):
        # url respects the newly found robots.txt
        urls.append(url) 
    return urls


def respects_robots(url, rules):
    parsed = urlparse(url)
    netloc = parsed.netloc
    if netloc not in rules:
        return True
    
    allowed = rules[netloc][0]
    disallowed = rules[netloc][1]

    for disallowed_path in disallowed:
        if parsed.path.startswith(disallowed_path):
            # if it looks like a disallowed path, look for any Allows rule
            return any(
                (parsed.path.startswith(allowed_path) for allowed_path in allowed)
                )
    return True # not disallowed anywhere, so it respects robots.txt

def _process_robots(resp: Response, rules: dict[str, tuple[list[str], list[str]]]) -> list[str]:
    extracted_urls = list()
    netloc = urlparse(resp.url).netloc
    for line in resp.raw_response.text.split('\n'):
        match line.split():
            case ['Sitemap:', site]:
                extracted_urls.append(site)
            case ['Allow:', path]:
                rules[netloc][0].append(path)
            case ['Disallow:', path]:
                rules[netloc][1].append(path)
    return extracted_urls
