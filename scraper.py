import re
from urllib.parse import urlparse
import urllib
from urllib.request import urlopen
from html.parser import HTMLParser

#this function receives a URL and corresponding web response
#(for example, the first one will be "http://www.ics.uci.edu" and the Web response will contain the page itself).
def scraper(url, resp):
    links = []
    if is_valid(url):
        response = resp
        #if response.status>=600 and response.status<=609:
            #TODO -> error
        if response.status >=200 and response.status <=599:
            #TODO ->success
            links.append(resp.url)
        
    #if it's a valid page 
    #parse the web response and extract enough information
    #you can also save the URL and the web page on your local disk.
    links = extract_next_links(url, resp)
    #return the list of URLs "scapped" from that page
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation requred.
    validStatusCodes = [200,301,302,307]
    outputLinks = list()
    if is_valid(url) and resp.error == None:
        outputLinks.append(url)
    
    while True:
        '''
        Open the URL/HTML text file. Find valid URL links and then
        puts it in outputLinks
        '''
        url = urlopen("https://www.pythonforbeginners.com/code/regular-expression-re-findall")
        break
    return outputLinks

def is_valid(url):
    try:
        #check if it is within the domains and paths (*.ics.uci.edu/*, *.cs.uci.edu/*, *.informatics.uci.edu/*, *.stat.uci.edu/*, 
        #today.uci.edu/department/information_computer_sciences/* )
        parsed = urlparse(url)
        valids = ["ics.uci.edu/","cs.uci.edu/","information.ics.edu/","stat.uci.edu/"]
        validStr = "".join(valids)
        url_netlock = parsed.netloc
        if not url_netlock.find(validStr):
            return false
        if parsed.scheme in set(["http", "https"]):
            return false
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
