import re
from urllib.parse import urlparse,urldefrag
import urllib
from bs4 import BeautifulSoup


#this is a set of crawled urls
already_crawled = set()
#this function receives a URL and corresponding web response
#(for example, the first one will be "http://www.ics.uci.edu" and the Web response will contain the page itself).
def scraper(url, resp):
    links = extract_next_links(url, resp)
    #return the list of URLs "scapped" from that page
    return [link for link in links if is_valid(link)]



def extract_next_links(url, resp):
    # Implementation requred.
    outputLinks = list()
    parsed = urlparse(url)
    #replaced resp.status condition with a function that checks it instead so
    #the code won't be as messy.
    if is_valid(url) and 200<=resp.status<=202 and checkIfAlreadyCrawled(url):
        html_doc = resp.raw_response.content
        soup = BeautifulSoup(html_doc, 'html.parser')
        for path in soup.find_all('a'):
            link = urllib.parse.urljoin(parsed.netloc, path.get('href'))
            outputLinks.append(urldefrag(link)[0])
    #checking for links in redirects with response 3xx
    if is_valid(url) and 300 <= resp.status <= 302:
        if resp.raw_response.history.length != 0:
            for link in resp.raw_response.history:
                fullUrl = urllib.parse.urljoin(parsed.netloc, link.url)
                outputLinks.append(urldefrag(fullUrl)[0])
                print("Adding redirect to list of extracted links")
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
    valids = ["ics.uci.edu","cs.uci.edu","information.ics.edu",
              "stat.uci.edu","informatics.uci.edu"]
    #only domain that has to check path as well, so i made it a separate if statement
    if url.netloc.strip('www.') == "today.uci.edu" and \
       "/department/information_computer_sciences" in url.path:
        return True 
    else:
        for domain in valids:
            if domain in url.netloc.strip('www.'):
                return True
    return False


def is_valid(url):
    try:
        #check if it is within the domains and paths (*.ics.uci.edu/*, *.cs.uci.edu/*, *.informatics.uci.edu/*, *.stat.uci.edu/*, 
        #today.uci.edu/department/information_computer_sciences/* )
        parsed = urlparse(url)
        
        #replaced with helper function to deal with netloc match
        if not checkNetloc(parsed.netloc):
            return False
        
        if parsed.scheme not in set(["http", "https"]):
            return False
        
        dontCrawled =["css","js","bmp","gif","jpeg","ico","png","tiff",
                      "mid","mp2","mp3","mp4","wav","avi","mov","mpeg","ram",
                      "m4v","mkv","ogg","ogv","pdf","ps","eps","tex","ppt",
                      "pptx","doc","docx","xls","xlsx|names","data","dat",
                      "exe","bz2","tar","msi","bin","7z","psd","dmg","iso",
                      "epub","dll","cnf","tgz","sha1","thmx","mso","arff",
                      "rtf","jar","csv","rm","smil","wmv","swf","wma","zip",
                      "rar","gz","svg","txt","py","rkt","ss","scm", "json",
                      "pdf"]

        for n in dontCrawled:
            if (n) in parsed.query or (n) in parsed.path:
                return False
				
        if "calendar" in parsed.path:
            return False


        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz|svg"
            + r"|txt|py|rkt|ss|scm|odc|sas)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise
	
