import bs4
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
from collections import deque
import requests

#visited crawls
visited = set()
#output files
bmc_url = 'https://www.brynmawr.edu'

#is this url valid?
def url_valid(url):
    try:
        print("checking if uclient can open url")
        uClient = uReq(url)
    except:
        pass
        return False
    return True
#given a url, create a Soup object that allows us to peak into HTML
def create_soup(url):
    print("creating soup...")
    #set up starting URL
    uClient = uReq(url)
    print("uclient opening up url")
    #loading html
    page_html = uClient.read()
    print("loading html")
    #close connection
    uClient.close()
    print("close connection")
    # load  html into soup
    page_soup = soup(page_html, "html.parser",from_encoding="iso-8859-1")
    print("load html into beautiful soup object")
    return page_soup

def print_set(input):
     #print links set
    print("Printing links set")
    for link in input:
        print(link)

#get headers and write to crawler.txt
def write_to_csv (url):
    res = requests.head(url)
    print("opening up url to get headers")
    header = dict (res.headers)
    if ('Last-Modified' in header.keys()):
        last_modified = header['Last-Modified'].replace(',','')
    else:
        last_modified = "N/A"
    if ('Content-Length' in header.keys()):
        size = str(header ['Content-Length'])
    else:
        size = "N/A"
        print("found last modified date..")
    line = url + ' , ' + size + ' , ' + last_modified
    print("return line", line)
    return line


#given a url, get all of the links in that web page and add to links set
def crawl_page(parent_url,links,visited,addedtocsv,file):
    print("CRAWLING URL " + parent_url + "/n")
    visited.add(parent_url)
    print("add to visited set")
    page_soup = create_soup(parent_url)
    #get all links
    for link in page_soup.findAll('a'):
        url = link.get('href')
        if (url is None):
            print("no url found in this a tag")
            continue
        if (url is not None):
            #if it starts with a backlash then it must be a site within the site
            print("url found:" + url)
            if (url.startswith("/")):
                #contruct full url
                url = bmc_url + url

            #hashtag indicates link same page
            if (url.startswith("#")):
                continue
        #only add links that are in the brynmawr.edu domain
        if ("brynmawr.edu" in url):
            print("found brynmawr.edu url" + url)
            if (url.startswith("http")):
                print("found http url" + url)
                if (url not in visited):
                    print ("added to links set since hasn't been visited", url)
                    links.add(url)
                    #write to csv file
                    if (url not in addedtocsv):
                        print("hasn't been added to file yet")
                        line = write_to_csv(url)
                        file.write(line + '\n')
                        print("WRITING to file..", url)
                        addedtocsv.add(url)
    print("FINISHED CRAWLING URL" + parent_url)

def main():
    print("STARTING program....")
    links = set([bmc_url])
    visited = set([bmc_url])
    addedtocsv = set()
    #while there are still urls to crawl
    with open("crawling_take_2.txt", "w+") as f:
        while (len(links) != 0):
            try:
                url = links.pop()
                print("popped url:"+url)
                #first make sure that url can be opened
                if (url_valid(url)):
                    print("valid url")
                    crawl_page(url,links,visited,addedtocsv,f)
            except:
                pass
if __name__ == "__main__":
    main()
