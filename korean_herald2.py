import numpy as np
import pandas as pd
import re
import requests
from urllib.request import urlopen as uReq
import sys
import httplib2
from bs4 import SoupStrainer, BeautifulSoup as soup
from httplib2 import RedirectLimit
import time
import nltk
import io
#from google.colab import drive
#from google.colab import files
import warnings
warnings.filterwarnings("ignore")
from datetime import date,datetime, timedelta
from lxml import etree
try:
    import datefinder
except:
    import datefinder
nltk.download('punkt')
try:
    from newspaper import Article
except:
    from newspaper import Article

my_url = "http://www.koreaherald.com/list.php?ct=020000000000&np=1&mp=1"
unique_page_links = []
user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,}
news_source_name="Korean Herald"

page_links = []
def fin_links(links):
    for lk in links:
        if lk not in unique_page_links:
             unique_page_links.append(lk)
    return

for i in range(10):
    http = httplib2.Http()
    count = 0
    page_links = []
    actual_link='http://www.koreaherald.com/list.php?ct=020000000000&np='+str(i)+'&mp=1'
    actual_link=actual_link + str(i)
    #status, response = http.request(actual_link)
    try:
        status, response = http.request(actual_link)
        for link in soup(response, 'html.parser', parseOnlyThese=SoupStrainer('a')):
            if link.has_attr('href'):
                if link is not None and link['href'][0:10]=="/view.php?":
                    page_links.append(link['href'])
    except (RedirectLimit, httplib2.ServerNotFoundError, UnicodeError, httplib2.RelativeURIError):
        pass
    fin_links(page_links)

unique_page_links1=[]
for link in unique_page_links:
     link='http://www.koreaherald.com'+link
     unique_page_links1.append(link)
print("No. of Unique Links : ", len(unique_page_links1))

templinks = unique_page_links1

for i in range (len(unique_page_links1)):
    auth = ""
    url = unique_page_links1[i]
    article = Article(url)
    article.download()
    article.parse()
    article.nlp()
    page = requests.get(url)
    soup1 = soup(page.content, 'html.parser')
    result_blog = soup1.find("div", {"class": "view_tit_byline_l"})
    auth="Author:"+result_blog.text+"\n"
    src = "Source:"+news_source_name+"\n"
    lnk = "Link:"+url+"\n"
    doe = "DateOfExtraction:"+datetime.today().strftime('%Y-%m-%d')+"\n"
    try:
        dop = str(date.strftime(datetime.strptime(article.publish_date, " %b %d, %y"), '%Y-%m-%d'))
    except:
        try:
            dop = str(datetime.strptime(article.publish_date, "%b %d, %Y").strftime('%Y-%m-%d'))
        except:
            dop = str(datetime.today().strftime('%Y-%m-%d'))
    ttl = "Title:"+article.title+"\n"
    '''
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
    '''
    try:
        filename=""+dop+" "+article.title+'.txt'
    except:
        filename=""+dop+" "+article.title+'.txt'
    article.text = re.sub(r'\n\n\n+', '\n', article.text)
    filename = re.sub(r'[@!%^*"()<>?/\|\t}{~:]', '', filename)
    print(filename)
    with io.open(filename, "w", encoding="utf-8") as f:
        f.write(src)
        f.write(lnk)
        f.write(doe)
        f.write(f"DateOfPublication:{dop}\n")
        f.write(ttl)
        f.write(auth)
        f.write("Article:")
        f.write(article.text)
        f.close()
        #files.download(filename)

#!zip -r /content/kh1.zip /content
#files.download("/content/kh1.zip")