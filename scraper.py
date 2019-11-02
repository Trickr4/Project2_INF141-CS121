import re
from urllib.parse import urlparse,urldefrag
import urllib
from bs4 import BeautifulSoup
import operator

#this is a set of crawled urls
already_crawled = set()
#variable for no 2
longestPage= 0
#dict for no 3
wordDict = {}
content={}
longestPage={}
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
    domain = "https://"+parsed.netloc
    words = []
    #writing urls into .txt files
    with open("url.txt", "a", encoding="utf-8") as file, \
         open("content.txt", "a", encoding="utf-8") as file2, \
         open("longest.txt","a",encoding="utf-8") as file3:

	#checks for valid url and response status
        if is_valid(url) and 200<=resp.status<=202 and checkIfAlreadyCrawled(url):
            html_doc = resp.raw_response.content
            soup = BeautifulSoup(html_doc, 'html.parser')
            #no2(url, soup)
            file.write(url+"\n")
            for t in soup.text.split():
                if t!="" and t.isalnum() and "[]" not in t:
               
                    words.append(t)
           
            longestPage[url]=len(words)
            file2.write(url+"\n"+str(words)+"\n")
            file3.write(url+"\n"+str(longestPage[url])+"\n")
            for path in soup.find_all('a'):
                relative = path.get('href')
                link = urllib.parse.urljoin(domain, relative)
                outputLinks.append(urldefrag(link)[0])
                file.write(urldefrag(link)[0]+"\n")
                
    file.close()
    file2.close()
    file3.close()
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
    
    valids = ["ics.uci.edu","cs.uci.edu", "stat.uci.edu",
              "informatics.uci.edu"]

    netloc = url.netloc

    subdomain = netloc

    if netloc.startswith("www."):
        netloc = netloc.strip("www.")

    netlist = netloc.split(".")
        
    if len(netlist) >= 4:
        subdomain = ".".join(netlist[1:])
    
    if netloc == "wics.ics.uci.edu" and \
       "/events" in url.path:
        return False

    if netloc == "archive.ics.uci.edu":
        return False

    if netloc == "hack.ics.uci.edu" and \
       "gallery" in url.path:
        return False

    if netloc == "grape.ics.uci.edu":
        return False

    if netloc == "intranet.ics.uci.edu":
        return False

    for domain in valids:
        if subdomain == domain:
            return True
        
    #only domain that has to check path as well, so i made it a separate if statement
    if netloc == "today.uci.edu" and \
       "/department/information_computer_sciences" in url.path:
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
        
        dontCrawled =["css","js","bmp","gif","jpeg","ico","png","tiff",
                      "mid","mp2","mp3","mp4","wav","avi","mov","mpeg","ram",
                      "m4v","mkv","ogg","ogv","pdf","ps","eps","tex","ppt",
                      "pptx","doc","docx","xls","xlsx|names","data","dat",
                      "exe","bz2","tar","msi","bin","7z","psd","dmg","iso",
                      "epub","dll","cnf","tgz","sha1","thmx","mso","arff",
                      "rtf","jar","csv","rm","smil","wmv","swf","wma","zip",
                      "rar","gz","svg","txt","py","rkt","ss","scm", "json",
                      "pdf", "wp-content", "calendar", "ical", "war", "img"]

        for n in dontCrawled:
            if (n) in parsed.query or (n) in parsed.path:
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
            + r"|txt|py|rkt|ss|scm|odc|sas|war|r|rmd"
            + r"|ds|apk|img)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise


'''
#answering no 2
def no2(url, html):
    text = html.get_text().split()
    words = []
    global longestPage
    for t in text:
        if t!="" and t.isalnum() and "[]" not in t:
            words.append(t)
    if len(words) > longestPage:
        longestPage = len(words)
        with open("longest.txt", "w", encoding="utf-8") as file:
            file.write(url+"\n")
            file.write(html.get_text())
        file.close()
	
'''
