# -*- coding: utf-8 -*-
import codecs
import sys
from bs4 import BeautifulSoup as bs
from requests import ConnectionError
import requests
import ssl
#from dbhandler import *
import time

headers={'Accept-Encoding': '*','Accept': '*/*', 'User-Agent': 'Mozilla 5.0'}
ssl._create_default_https_context = ssl._create_unverified_context

def GetPage():
    url="https://www.denvergov.org/content/denvergov/en/denver-development-services/help-me-find-/building-permits.html"
    req = requests.get(url,headers=headers)
    page = req.text
    soup = bs(page,"lxml")
    return soup

page = GetPage()
links = page.find_all('a',href=True)
for link in links:
    path=link.get('href')
    if "xls" in path:
        print path
