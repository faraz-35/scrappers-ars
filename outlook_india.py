import numpy as np
import pandas as pd
import re
import requests
import urllib.request
from urllib.request import urlopen as uReq
import sys
import time
import httplib2
from bs4 import SoupStrainer, BeautifulSoup as soup
from httplib2 import RedirectLimit
from lxml import etree
import io
#from google.colab import drive
#from google.colab import files
from newspaper import Article
import warnings
warnings.filterwarnings("ignore")
from datetime import date,datetime, timedelta
try:
    import datefinder
except:
    !pip install datefinder
    import datefinder

unique_page_links = []
my_url = "https://www.outlookindia.com/website/"
#user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36 OPR/76.0.4017.107'
headers={'User-Agent':user_agent,}
yesterday = datetime.now() - timedelta(1)
yesterday = datetime.strftime(yesterday, '%Y/%m/%d')
monthYear = yesterday[:-3]
year = yesterday[:-6]
source = "Outlook India"

def fin_links(links):
    for lk in links:
        if lk not in unique_page_links: 
            unique_page_links.append(lk)
    return

page_links = []
for i in range(10):
	http = httplib2.Http()
	page_links = []
	actual_link='https://www.outlookindia.com/website/'
	actual_link=actual_link + str(i)
	status, response = http.request(actual_link)
	for link in soup(response, 'html.parser', parseOnlyThese=SoupStrainer('a')):
		if link.has_attr('href'):
			if link is not None and link['href'][0:15]=="/website/story/":
				page_links.append(link['href'])
	fin_links(page_links)
print("No. of Unique links : ", len(unique_page_links))

unique_page_links1=[]
for link in unique_page_links:
	link='https://www.outlookindia.com/'+link
	unique_page_links1.append(link)
unique_page_links1
print("No. of Unique Links : ", len(unique_page_links1))

unique_page_links1

from bs4 import BeautifulSoup
Previous_Date = date.today()
Previous_Date=Previous_Date.strftime("%d %B %Y")
date_of_extraction=date.today().strftime("%Y-%m-%d")
for index,link in enumerate(unique_page_links1):
  page = requests.get(link)
  soup1 = BeautifulSoup(page.content, 'html.parser')
  result_heading = soup1.find("h1", {"itemprop": "headline"})
  if result_heading is not None:
    Title=result_heading.text
    result_blog = soup1.find("div", {"class": "author_name_date"})
    author_name=result_blog.find("span")
    dom = etree.HTML(str(soup1))
    date_of_publication=dom.xpath('//*[@id="web_page"]/div[1]/div[3]/div[1]/div[2]/text()')
    date_of_publication=date_of_publication[-1]
    have_author=True
    if author_name is not None:
      author=author_name.text
    else:
      have_author=False
      author="Not mentioned"
    result_blog=result_blog.text
    blog_text1 = result_blog.splitlines()
    date_of_publication = re.sub(r"[\t]*", "", date_of_publication)
    first_text=soup1.find("div", {"class": "wrapper_story_left"})
    first_text=first_text.find('h4')
    first_text=first_text.text
    all_other_paragraphs=soup1.find("div", {"itemprop": "articleBody"})
    all_other_paragraphs=all_other_paragraphs.find_all('p')
    text=[]
    for node in all_other_paragraphs:
      line=node.find(text=True)
      if line is not None:
        text.append(line)
    if text is not None:
      texts1=''.join(text)
      first_text=first_text+texts1
      blog_text = first_text.replace(u'\xa0', u'')
      Title=str(Title)
      try:
          dop = str(date.strftime(datetime.strptime(date_of_publication, " %d %B %Y"), '%Y-%m-%d'))
      except:
          #print(date_of_publication)
          if(date_of_publication is not None):
              matches = list(datefinder.find_dates(date_of_publication))
              if len(matches) > 0:
                  temp_dop = matches[0]
                  #print(temp_dop)
                  temp = temp_dop.strftime('%Y-%m-%d')
                  #print(temp)
              dop = temp
          else:
            pass
      filename=dop+" "+Title+'.txt'
      filename = re.sub(r'[@^*"()<>?/\|\t}{~:]', '', filename)
      author = re.sub(r'\n', '', author)
      print(filename, index)
      f=open(filename,'w+', encoding="utf-8")
      f.write(f"Source:{source}\n")
      f.write(f"Link:{link}\n")  
      f.write(f"DateOfExtraction:{date_of_extraction}\n")
      f.write(f"DateOfPublication:{dop}\n")
      f.write(f"Title:{Title}\n")
      f.write(f'Author:{author}\n')
      f.write(f"Article:{blog_text}\n")
      f.close()
      #files.download(filename)

#!zip -r /content/out.zip /content
#files.download("/content/out.zip")
