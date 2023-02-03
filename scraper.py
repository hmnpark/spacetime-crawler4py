import re
from urllib.parse import urlparse, urldefrag

# Import parse libraries.
from bs4 import BeautifulSoup
from lxml import html

# Import tokenizer.
from utils.tokenize import computeWordFrequencies

# Import information content filter.
from utils.content_filter import has_high_textual_information_content

MAX_SIZE = 15_000_000

def scraper(url, resp, frontier):
    match resp.raw_response:
        case None:
            frontier.report.add_page(url, {})
            return []
        case _:
            page_text = BeautifulSoup(resp.raw_response.content, 'html.parser')
            frequencies = computeWordFrequencies(page_text.get_text())
            frontier.report.add_page(url, frequencies)
            if not has_high_textual_information_content(frequencies): return []
            elif frontier.simhash.is_similar(resp, frequencies): return []
            links = extract_next_links(url, resp)
            return [urldefrag(link).url for link in links if is_valid(link)]


def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    match resp.status:
        case 200:
            if len(resp.raw_response.content) <= MAX_SIZE:
                return [link[2] for link in html.iterlinks(resp.raw_response.content)]
            return []
        case _: return []

def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return/admissions/undergraduate-application-process/ False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        elif not parsed.netloc.endswith((".ics.uci.edu",
                                         ".cs.uci.edu",
                                         ".informatics.uci.edu",
                                         ".stat.uci.edu")) \
            or re.match(r'\?share=twitter|\?share=facebook|wp-json', url):
            return False
        # handle ?share=twitter, ?share=facebook, wp-json
        # elif re.match(r'\?share=twitter|\?share=facebook|wp-json', url):
        #     return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
