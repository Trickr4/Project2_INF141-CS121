import re
from urllib.parse import urlparse,urldefrag
import urllib
from bs4 import BeautifulSoup
import operator
from collections import defaultdict

#this is a set of crawled urls
already_crawled = set()
#list for no 1
unique = []
#variable for no 2
longestPage= 0
#dict for no 3
wordDict = {}

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

    #writing urls into url.txt
    with open("url.txt", "a", encoding="utf-8") as file:
	       
    #replaced resp.status condition with a function that checks it instead so
    #the code won't be as messy.

        if is_valid(url) and 200<=resp.status<=202 and checkIfAlreadyCrawled(url):
            html_doc = resp.raw_response.content
            soup = BeautifulSoup(html_doc, 'html.parser')
            no1(url)
            no2(url, soup)
            file.write(url)
            file.write("\n")
            file.write("Number of unique urls: "+str(len(unique))+"\n")
            for path in soup.find_all('a'):
                link = urllib.parse.urljoin(parsed.netloc, path.get('href'))
                outputLinks.append(urldefrag(link)[0])
                file.write(urldefrag(link)[0])
                file.write("\n")
                
        #checking for links in redirects with response 3xx
        if is_valid(url) and 300 <= resp.status <= 302:
            file.write(url)
            file.write("\n")
            if resp.raw_response.history.length != 0:
                for link in resp.raw_response.history:
                    fullUrl = urllib.parse.urljoin(parsed.netloc, link.url)
                    outputLinks.append(urldefrag(fullUrl)[0])
                    file.write(urldefrag(link)[0])
                    file.write("\n")
                
    file.close()
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

    for domain in valids:
        if domain in url.netloc.strip('www.'):
            return True
        
    #only domain that has to check path as well, so i made it a separate if statement
    if url.netloc.strip('www.') == "today.uci.edu" and \
       "/department/information_computer_sciences" in url.path:
        return True
    
    if url.netloc.strip('www.') == "wics.ics.uci.edu" and \
       "/events" in url.path:
        return False

    if url.netloc.strip('www.') == "archive.uci.edu":
        return False
        
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
                      "pdf", "wp-content", "calendar", "ical", "war"]

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
            + r"|txt|py|rkt|ss|scm|odc|sas|war)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise


#answering no 1
def no1(urls):
    parsed = urlparse(url)
    net =parsed.netloc
    if net not in unique:
        unique.append(net)


#answering no 2
def no2(url, html):
    text = html.text().split()
    words = []
    for t in soup.text.split():
        if t!="" and t.isalnum() and "[]" not in t:
            words.append(t)
    if len(words) > longestPage:
        longestPage = len(words)
        with open(str(url)+".txt", "w", encoding="utf-8") as file:
            file.write(html.text())
    file.close()


#answering no 3
def no3(urls):
    print("no 3")
    allWords= []
    for url in urls:
        resp = requests.get(url).text
        soup = BeautifulSoup(resp, 'html.parser')
        for t in soup.text.split():
            if t!="" and t.isalnum() and "[]" not in t:
                allWords.append(t)
    
    for word in allWords:
        word = word.lower()
        if word in wordDict:
            wordDict[word]+=1
        else:
            wordDict[word]=1
    most50Words = []
    for i in range(0,50):
        most = max(wordDict.items(),key = operator.itemgetter(1))[0]
        most50Words.append(most)
        del wordDict[most]
    print("50 most appear words ",most50Words)


#answering no 4
def no4(urls):
    print("no 4")
    subdomains = defaultdict(int)
    for url in urls:
        parsed = urlparse(url)
        if 'ics.uci.edu' in parsed.netloc.strip('www.'):
            subdomains[parsed.netloc]+=1

    print("Number of subdomains in ics.uci.edu domain: "+ \
          str(len(subdomains)))
    for key,value in subdomains.items():
        print(key + str(value))
	
