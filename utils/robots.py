import time
from logging import Logger
from urllib.parse import urlparse

from utils.response import Response
from utils.config import Config
from utils.download import download


# rules example dict:
#   dict{netloc: ([list of allowed paths], [list of disallowed paths])}


def robots_check(
    url: str,
    rules: dict[str, tuple[list[str], list[str]]],
    config: Config, logger: Logger=None
    ) -> list[str]:
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
    rules[parsed.netloc] = ([], []) # no robots.txt rules to follow. allow all.
    if resp.status != 200:
        return [url]    # no robots.txt to process
    
    urls = _process_robots(resp, rules)
    if respects_robots(url, rules):
        # url respects the newly found robots.txt
        urls.append(url) 
    return urls


def respects_robots(
    url: str,
    rules: dict[str, (list[str], list[str])]
    ) -> bool:
    '''Checks if the url respects its authority's robots.txt.'''
    parsed = urlparse(url)
    netloc = parsed.netloc
    if netloc not in rules:
        # the rules will be updated in Frontier.add_url
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


def _process_robots(
    resp: Response,
    rules: dict[str, tuple[list[str], list[str]]]
    ) -> list[str]:
    '''
    Add an authority's robot.txt rules to the dict.
    Return a list of sitemap links.
    '''
    extracted_urls = list()
    netloc = urlparse(resp.url).netloc
    lines = resp.raw_response.text.split('\n')

    # find correct user-agent
    start_from_idx = 0
    for i in range(len(lines)):
        if lines[i] == 'User-agent: *':
            start_from_idx = i + 1 
    # start processing from user-agent
    for i in range(start_from_idx, len(lines)):
        match lines[i].split():
            case ['Sitemap:', site]:
                extracted_urls.append(site)
            case ['Allow:', path]:
                rules[netloc][0].append(path)
            case ['Disallow:', path]:
                rules[netloc][1].append(path)
    return extracted_urls
