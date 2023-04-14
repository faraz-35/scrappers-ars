import numpy
import pandas
import re
import io
import requests
import urllib.request 
from urllib.request import urlopen as uReq
import sys
import httplib2
from bs4 import SoupStrainer, BeautifulSoup as soup
from httplib2 import RedirectLimit
import time
from datetime import datetime, timedelta
#from google.colab import drive
#from google.colab import files
import warnings
warnings.filterwarnings("ignore")
import nltk
nltk.download('punkt')
try:
    from newspaper import Article
except:
    !pip install newspaper3k
    from newspaper import Article

my_url = "https://www.nytimes.com/"
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,} 
unique_page_links = []
yesterday = datetime.now() - timedelta(1)
yesterday = datetime.strftime(yesterday, '%Y/%m/%d')
yesyesterday = datetime.now() - timedelta(2)
yesyesterday = datetime.strftime(yesyesterday, '%Y/%m/%d')
monthYear = yesterday[:-3]
year = yesterday[:-6]
source = "The New York Times"
tempyesterday = datetime.strftime(datetime.now() - timedelta(1), '%Y/%m/%d')

def fin_links(links):
    for lk in links:
        if lk not in unique_page_links: 
            unique_page_links.append(lk)
    print("No. of unique links : ", len(unique_page_links))
    return

def checkLinksYestrday(ylinks):
    for lk in ylinks:
        if year not in lk:
            #if yesyesterday not in lk:
            ylinks.remove(lk)
    return

page_links = []
http = httplib2.Http()
count = 0
status, response = http.request('https://www.nytimes.com/international/')
for link in soup(response, 'html.parser', parseOnlyThese=SoupStrainer('a')):
    if link.has_attr('href'):
        if link is not None and link['href'][:24] == 'https://www.nytimes.com/':
                page_links.append(link['href'])
                count+=1
print("No. of links : ", len(page_links))
fin_links(page_links)

unique_page_links

sub_page_links = []
initial_links_size = len(unique_page_links)
updated_links_size = 0
j = 0
while (True):
    for lk in range(len(unique_page_links)-j):
        try:
            response = urllib.request.Request(unique_page_links[lk+j],None,headers)
            try:
                with urllib.request.urlopen(response) as response:
                    data = response.read()
            except:
                pass
        except (RedirectLimit, httplib2.ServerNotFoundError, UnicodeError, httplib2.RelativeURIError):
            break
        print(unique_page_links[lk+j])
        for link in soup(data, 'html.parser', parseOnlyThese=SoupStrainer('a')):
            if link.has_attr('href'):
                if link is not None and link['href'][:24] == 'https://www.nytimes.com/':
                    #if yesterday in link['href']:
                    #if year in link['href']:
                    if monthYear in link['href']:
                        sub_page_links.append(link['href'])
        print("No. of sub links : ", len(sub_page_links))
        if(lk+j>len(unique_page_links)):
            break
    fin_links(sub_page_links)
    updated_links_size = len(unique_page_links)
    if(updated_links_size == initial_links_size):
        break
    else:
        j = initial_links_size
        initial_links_size = len(unique_page_links)
print("\nTotal No. of links : ", len(unique_page_links))

templinks = unique_page_links

yesterdaylinks = unique_page_links
while(True):
    temp = len(yesterdaylinks)
    checkLinksYestrday(yesterdaylinks)
    if(temp == len(yesterdaylinks)):
        break
print("Total yesterday links : ", len(yesterdaylinks))

for i in range (len(yesterdaylinks)):
  try:
    auth = ""
    url = yesterdaylinks[i]
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    src = "Source:"+source+"\n"
    lnk = "Link:"+url+"\n"
    doe = "DateOfExtraction:"+datetime.today().strftime('%Y-%m-%d')+"\n"
    try:
        dop = "DateOfPublication:"+article.publish_date.strftime('%Y-%m-%d')+"\n"
    except:
        dop = "DateOfPublication:"+str(tempyesterday)+"\n"
    ttl = "Title:"+article.title+"\n"
    auth+="Author:"
    for i in range (len(article.authors)):
        auth += article.authors[i]
        auth += ","
    if auth[-1] == ",":
        auth = auth[:-1]+"\n"
    elif (auth[-1] == ':'):
        auth+="Not Mentioned"+"\n"
    else:
        auth+="\n"
    try:
        filename=""+article.publish_date.strftime('%Y-%m-%d')+" "+article.title+'.txt'
    except:
        filename=""+str(tempyesterday)+" "+article.title+'.txt'
    filename = re.sub(r'[@!%^*"()<>?/\|\t}{~:]', '', filename)
    print(filename)
    with io.open(filename, "w", encoding="utf-8") as f:
        f.write(src)
        f.write(lnk)
        f.write(doe)
        f.write(dop)
        f.write(ttl)
        f.write(auth)
        f.write("Article:")
        f.write(article.text)
        f.close()
        #files.download(filename)
  except:
    pass

#!zip -r /content/nyt.zip /content
#files.download("/content/nyt.zip")