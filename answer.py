from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import operator
from collections import defaultdict
import re
#dict for no 2
longestPage={}
#dict for no 3
wordDict = {}

#answeing no 1
def no1(urls):
    file =open("report.txt","a",encoding="utf8")
    uniqueUrl = set()
    for url in urls:
        if is_valid(url):
            uniqueUrl.add(url)
    countUnique = len(uniqueUrl)
    file.write("Number of unique urls: "+str(countUnique)+"\n")
    file.close()

	
#answering no 2
def no2(urls):
    file =open("report.txt","a",encoding="utf8")
    url = ""
    longest = 0
    for i in range(0, len(urls), 2):
        if int(urls[i+1]) > longest:
            url = urls[i]
            longest = int(urls[i+1])
    file.write("Url with the most words: "+url+"\n")
    file.write("Length of url with the most words: "+str(longest)+"\n")
    file.close()

    
#answering no 3
def no3(urls, stopWords):
    file =open("report.txt","a",encoding="utf8")
    for word_list in urls[1::2]:
        for word in word_list.strip().split(","):
            word = str(word.lower()).strip().replace("'", '')
            if word in wordDict:
                wordDict[word]+=1
            else:
                wordDict[word]=1
    for word in stopWords:
        if word in wordDict.keys():
            wordDict.pop(word)
    most50Words = []
    for i in range(0,50):
        most = max(wordDict.items(),key = operator.itemgetter(1))[0]
        most50Words.append(most)
        del wordDict[most]
    file.write("Top 50 words:\n")
    for word in most50Words:
        file.write(word+"\n")
    file.close()


#answering no 4
def no4(urls):
    file =open("report.txt","a",encoding="utf8")
    subdomains = defaultdict(int)
    for url in urls:
        parsed = urlparse(url)
        netloc = parsed.netloc
        if netloc.startswith("www."):
            netloc = netloc.strip('www.')
        netlist = netloc.split(".")
        subdomain = ".".join(netlist[1:])
        if subdomain == 'ics.uci.edu':
            subdomains[netloc]+=1

    file.write("Number of subdomains in ics.uci.edu domain: "+ \
               str(len(subdomains))+"\n")
    for key,value in subdomains.items():
        file.write(key +" "+ str(value)+"\n")
    file.close()


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


def main():
    print("starting main()")
    file =open("report.txt","a",encoding="utf8")
    file2 =open("url.txt","r", encoding="utf8")
    file3 =open("longest.txt","r", encoding="utf8")
    file4 =open("content.txt","r", encoding="utf8")
    file5 =open("stopWords.txt", "r", encoding="utf8")
    #urls that are crawled
    urls = []
    for n in file2:
        urls.append(n.rstrip())
    urls2 = []
    for n in file3:
        urls2.append(n.rstrip())
    content = []
    for n in file4:
        content.append(n.strip())
    stopwords = []
    for n in file5:
        stopwords.append(n.rstrip())
    no1(urls)
    no2(urls2)
    no3(content, stopwords)
    no4(urls)
    file2.close()


if __name__ == "__main__":
    main()
