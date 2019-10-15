import re
from urllib.parse import urlparse

#this function receives a URL and corresponding web response
#(for example, the first one will be "http://www.ics.uci.edu" and the Web response will contain the page itself).
def scraper(url, resp):
    if is_valid(url):
        response = resp
        if response.status>=600 and response.status<=609:
            #TODO -> error
        else if response.status >=200 and response.status <=599:
            #TODO ->success
        
    #if it's a valid page 
    #parse the web response and extract enough information
    #you can also save the URL and the web page on your local disk.
    links = extract_next_links(url, resp)
    #return the list of URLs "scapped" from that page
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    # Implementation requred.
    return list()

def is_valid(url):
    try:
        #check if it is within the domains and paths (*.ics.uci.edu/*, *.cs.uci.edu/*, *.informatics.uci.edu/*, *.stat.uci.edu/*, 
        #today.uci.edu/department/information_computer_sciences/* )
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
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
