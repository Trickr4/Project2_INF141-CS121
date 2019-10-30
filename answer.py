from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import operator
#dict for no 2
longestPage={}
#dict for no 3
wordDict = {}

#answeing no 1
def no1(urls):
    print("no1")
    uniqueUrl = []
    for url in urls:
        parsed = urlparse(url)
        net =parsed.netloc
        if net not in uniqueUrl:
            uniqueUrl.append(net)
    countUnique = len(uniqueUrl)
    print("unique url = ",countUnique)
	
#answering no 2
def no2(urls):
    print("no 2")
    for url in urls:
        words = []
        resp = requests.get(url).text
        soup = BeautifulSoup(resp, 'html.parser')
        
        for t in soup.text.split():
            if t!="" and t.isalnum() and "[]" not in t:
               
                words.append(t)
           
        longestPage[url]=len(words)
    maxWords =max(longestPage.items(),key = operator.itemgetter(1))[0]
    print("url with the most words=",maxWords)
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

def main():
    print("starting main()")
    file2 =open("url.txt","r")
    #urls that are crawled
    urls = []
    for n in file2:
        urls.append(n.rstrip())
    print(urls)
    no1(urls)
    no2(urls)
    no3(urls)	
    file2.close()
if __name__ == "__main__":
    main()
