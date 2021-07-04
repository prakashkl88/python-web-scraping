import re
import requests
from bs4 import BeautifulSoup

def in_stock(title, topic):
    baseURL = '' #<hidden, please add url here>
    page = requests.get(baseURL)

    soup = BeautifulSoup(page.content, 'html.parser') 
    divparent = soup.find_all('div', attrs={'class':'side_categories'})[0]

    #build the topics hash-map
    topics = {}
    for scrape in divparent.findAll('a'):
        key = str(scrape.text).replace("\n","").replace(" ","").lower()
        value = str(scrape.get('href'))
        topics[key] = value

    topicLower = topic.replace(" ","").lower()
    if topicLower not in topics.keys():
        return False
    topicURL = baseURL + topics[topicLower]
    #print(topicURL)
    
    bookSet = set([])
    def getBooks(topicURL):
        pageTopic = requests.get(topicURL)
        soupTopic = BeautifulSoup(pageTopic.content, 'html.parser')
        divparentTopic = soupTopic.find_all('h3')
    
        for book in divparentTopic:
            bookSet.add(str(book.findAll('a')[0].get('title')).lower())

    #check for multiple pages of books
    getBooks(topicURL)
    pageTopic = requests.get(topicURL)
    soupTopic = BeautifulSoup(pageTopic.content, 'html.parser')
    if len(soupTopic.find_all('ul', {'class': 'pager'})) > 0:
        txt = str(soupTopic.find_all('ul', {'class': 'pager'})[0].text)
        numPages = [int(s) for s in txt.split() if s.isdigit()][1]
        for i in range(2, numPages+1):
            htmlString = 'page-%s.html' % i
            newTopicURL = topicURL.replace("index.html", htmlString)
            getBooks(newTopicURL)
            
    titleLower = title.lower()
    if titleLower in bookSet:
        return True
    else:
        return False



## TESTING ##
print(in_stock("awkward","sequential art"))
#print(in_stock("The MooSEwood Cookbook: Recipes from Moosewood Restaurant, Ithaca, New York", "food and driNk"))
#print(in_stock("Online Marketing for Busy Authors: A Step-By-Step guide", "Self help"))
#print(in_stock("While You Were Mine", "Historical Fiction"))
#print(in_stock("While You Were Mine", "Science"))
