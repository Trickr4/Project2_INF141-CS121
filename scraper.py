import re
from urllib.parse import urlparse
import urllib
from urllib.request import urlopen
from html.parser import HTMLParser

#this function receives a URL and corresponding web response
#(for example, the first one will be "http://www.ics.uci.edu" and the Web response will contain the page itself).
def scraper(url, resp):
    links = extract_next_links(url, resp)
    #return the list of URLs "scapped" from that page
    return [link for link in links if is_valid(link)]


def extract_next_links(url, resp):
    # Implementation requred.
    outputLinks = list()
    htmlscript = []
    url_netloc = urlparse(url).netloc
    if is_valid(url) and 200 <= resp.status <= 599:
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
    already_crawled = set()
    if url not in already_crawled:
        already_crawled.add(url)
        return True
    return False


def is_valid(url):
    try:
        #check if it is within the domains and paths (*.ics.uci.edu/*, *.cs.uci.edu/*, *.informatics.uci.edu/*, *.stat.uci.edu/*, 
        #today.uci.edu/department/information_computer_sciences/* )
        parsed = urlparse(url)
        valids = ["ics.uci.edu/","cs.uci.edu/","information.ics.edu/","stat.uci.edu/"]
        validStr = "".join(valids)
        url_netlock = parsed.netloc
	
        if not checkIfAlreadyCrawled(url):
            return False

        #since netloc comes with www., it wasn't finding a match in validStr
        if not url_netlock[4::] in validStr:
            return False
        
        if parsed.scheme not in set(["http", "https"]):
            return False
        
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico|php"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|svg)$", parsed.path.lower())

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

    
    '''
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
        
    #Issue: URL have a path but no domain. This is technically consider inside the domain
    #Solution: Accept the URL but add the domain and scheme to the path.
    #  then added it to list of links.
if __name__ == '__main__':
    htmlscript = []
    req = urllib.request.Request("https://www.ics.uci.edu")
    url = urlopen(req)
    for line in url:
        htmlscript.append(str(line).strip('b\''))
    parser = MyHTMLParser()
    for line in htmlscript:
        parser.feed(line)
    for path in parser.get_links():
        #Using urllib.parse.urljoin fixes the issue where weird url links were
        #combined. Now all the url links seem to be formatted properly
        print(urllib.parse.urljoin("https://www.ics.uci.edu", path))
    '''
