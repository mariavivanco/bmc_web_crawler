import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from collections import deque

#set up starting URL  
myurl = 'https://www.brynmawr.edu'
uClient = uReq(myurl)
#loading html 
page_html = uClient.read()
#close connection 
uClient.close()
# load  html into soup
page_soup = soup(page_html, "html.parser")
links = set() 
totalLinks = 0
totalBMCLinks = 0

#get all links
for link in page_soup.find_all('a'):
    url = link.get('href')
    print("URL found", url)
    if (url is None):
        continue
    if (url is not None):
        #if it starts with a backlash then it must be a site within the site 
        if (url.startswith("/")):
            #contruct full url 
            url = myurl + url 
        #hashtag indicates link to the same page
        if (url.startswith("#")):
            continue 
        totalLinks = totalLinks + 1
    #only add links that are in the brynmawr.edu domain 
    if ("brynmawr.edu" in url): 
        links.add(url)
totalBMCLinks = len(links)    
#print links set
print("Printing links set")
for link in links:
    print(link) 
print("total number of bmc links on first page: " + str(totalBMCLinks))
print ("total number of links in general on first page" + str(totalLinks))
    