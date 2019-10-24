import re
from urllib.parse import urlparse
import urllib
from urllib.request import urlopen
from html.parser import HTMLParser

#this is a set of crawled urls
already_crawled = set()
#this function receives a URL and corresponding web response
#(for example, the first one will be "http://www.ics.uci.edu" and the Web response will contain the page itself).
def scraper(url, resp):
    links = extract_next_links(url, resp)
    #return the list of URLs "scapped" from that page
    return [link for link in links if is_valid(link)]


#function used to identify response status
def valid_resp(resp):
    if 200 <= resp.status <= 202:
        return True 
    elif 300 <= resp.status <=304 or resp.status == 307:
        return True 
    else:
        return False


def extract_next_links(url, resp):
    # Implementation requred.
    outputLinks = list()
    htmlscript = []
    url_netloc = urlparse(url).netloc
    #replaced resp.status condition with a function that checks it instead so
    #the code won't be as messy.
    if is_valid(url) and valid_resp(resp) and checkIfAlreadyCrawled(url):
        req = urllib.request.Request(url)
        link = urlopen(req)
        for line in link:
            htmlscript.append(str(line).strip('b\''))
        parser = MyHTMLParser()
        for line in htmlscript:
            parser.feed(line)
        for path in parser.get_links():
            outputLinks.append(urllib.parse.urljoin(url_netloc, path, allow_fragments=False))
    return outputLinks


#function to check if the url is crawled already
def checkIfAlreadyCrawled(url):
    if url[-1]=="/":
	    url = url[:-1]
    if url not in already_crawled:  
        already_crawled.add(url)
        return True
    return False


#function to check if url netloc matches url domains we are allowed to crawl
def checkDomain(url):
    valids = ["ics.uci.edu","cs.uci.edu","information.ics.edu","stat.uci.edu","informatics.uci.edu"]
    #only domain that has to check path as well, so i made it a separate if statement
    if url.netloc.strip('www.') == "today.uci.edu" and \
       "/department/information_computer_sciences" in url.path:
        return True 
    else:
        for domain in valids:
            if domain in url.netloc.strip('www.'):
                return True
    return False


#function to check if the path has any invalid file extensions
def checkPath(path):
    invalids = ["json", "pdf"] 
    for word in invalids:
        if word in path:
                return True 
    return False 


def is_valid(url):
    try:
        #check if it is within the domains and paths (*.ics.uci.edu/*, *.cs.uci.edu/*, *.informatics.uci.edu/*, *.stat.uci.edu/*, 
        #today.uci.edu/department/information_computer_sciences/* )
        parsed = urlparse(url)
        
        #replaced with helper function to deal with netloc match
        if not checkDomain(parsed):
            return False
        
        if parsed.scheme not in set(["http", "https"]):
            return False

        if checkPath(parsed.path.lower()):
        	return False
        
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico|php"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|svg"
            + r"|txt|py|rkt|ss|scm)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise


class MyHTMLParser(HTMLParser):
    def reset(self):
        HTMLParser.reset(self)
        self.links = []
        
    def handle_starttag(self, tag, attrs):
        for content in attrs:
            if "href" in content:
                self.links.append(content[1].strip("\\'"))
                
    def get_links(self):
        return self.links
