import numpy
import pandas
import re
import requests
import urllib.request 
from urllib.request import urlopen as uReq
import sys
import httplib2
from bs4 import SoupStrainer, BeautifulSoup as soup
from httplib2 import RedirectLimit
#from google.colab import drive
#from google.colab import files
import warnings
warnings.filterwarnings("ignore")
import time
from datetime import datetime, timedelta
import nltk
from datetime import datetime
from bs4 import BeautifulSoup
import io
nltk.download('punkt')
try:
    from newspaper import Article
except:
    from newspaper import Article

unique_page_links = []
my_url = "https://nationalinterest.org/recent-stories?page=0"
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,}
yesterday = datetime.now() - timedelta(1)
yesterday = datetime.strftime(yesterday, '%Y/%m/%d')
monthYear = yesterday[:-3]
year = yesterday[:-6]
source = "The National Interest"

def fin_links(links):
    for lk in links:
        if lk not in unique_page_links: 
            unique_page_links.append(lk)
    return
blogs_list=['/blog/the-skeptics','/blog/the-buzz','/blog/paul-pillar','/blog/middle-east-watch','/blog/korea-watch']

page_links = []
count = 0
for i in range(15):
  http = httplib2.Http()
  count = 0
  page_links = []
  actual_link='https://nationalinterest.org/recent-stories?page='
  actual_link=actual_link + str(i)
  status, response = http.request(actual_link)
  for link in soup(response, 'html.parser', parseOnlyThese=SoupStrainer('a')):
    if link.has_attr('href'):
      if link is not None and link['href'][0:6]=="/blog/":
        if link['href'] not in blogs_list:
          page_links.append(link['href'])
  fin_links(page_links)

unique_page_links1=[]
for link in unique_page_links:
  link='https://nationalinterest.org'+link
  unique_page_links1.append(link)
print("No. of unique links : ", len(unique_page_links1))

unique_page_links1

for i in range (len(unique_page_links1)):
    url = unique_page_links1[i]
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    src = "Source:"+source+"\n"
    lnk = "Link:"+url+"\n" 
    doe = "DateOfExtraction:"+datetime.today().strftime('%Y-%m-%d')+"\n"
    # dop = "DateOfPublication:"+article.publish_date.strftime('%Y-%m-%d')+"\n"
    dop = "DateOfPublicati0on:"+article.publish_date.strftime('%Y-%m-%d') if(article.publish_date) else '2023-03-12' +"\n"
    ttl = "Title:"+article.title+"\n"
    auth = "Author:"
    page = requests.get(url)
    soup1 = BeautifulSoup(page.content, 'html.parser')
    result_blog = soup1.find("span", {"class": "meta__author"})
    try:
        author_name=result_blog.find("a")
        auth+=author_name.text
    except:
        auth+="Not Mentioned"
    #for i in range (len(article.authors)):
        #auth += article.authors[i]
        #auth += ","
    #auth = auth[:-1]+"\n"
    auth+="\n"
    # filename=""+article.publish_date.strftime('%Y-%m-%d')+" "+article.title+'.txt'
    filename= ""+article.publish_date.strftime('%Y-%m-%d') if(article.publish_date) else '2023-03-12'
    filename = re.sub(r'[@^*"()<>?/\|\t}{~:]', '', filename)
    
    # print(filename)
    # with io.open(filename, "w", encoding="utf-8") as f:
    #     f.write(src)
    #     f.write(lnk)
    #     f.write(doe)
    #     f.write(dop)
    #     f.write(ttl)
    #     f.write(auth)
    #     f.write("Article:")
    #     f.write(article.text)
    #     f.close()

#!zip -r /content/tni.zip /content
#files.download("/content/tni.zip")