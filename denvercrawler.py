# -*- coding: utf-8 -*-
from __future__ import print_function
import codecs
import sys
from bs4 import BeautifulSoup as bs
from requests import ConnectionError
import requests
import ssl
import os
import shutil
import time
import urllib2
import pandas

#dummy headers to make pages trust our evil crawler
headers={'Accept-Encoding': '*','Accept': '*/*', 'User-Agent': 'Mozilla 5.0'}
ssl._create_default_https_context = ssl._create_unverified_context

#this is the page we want to scrape and soupify
def GetPage():
    url="https://www.denvergov.org/content/denvergov/en/denver-development-services/help-me-find-/building-permits.html"
    req = requests.get(url,headers=headers)
    page = req.text
    soup = bs(page,"lxml")
    return soup

#let's find .xls on this page
def GetLinks():
    page = GetPage()
    links = page.find_all('a',href=True)
    for link in links:
        path=link.get('href')
        if "xls" in path:
            filename=link.get_text().replace(" ", "").replace("/","-")+".xls"
            if "http" in path:
                SaveFile(path,filename)
            else:
                domain="https://www.denvergov.org"
                path=domain+path
                SaveFile(path,filename)

#save those files
def SaveFile(path,filename):
    req = urllib2.urlopen(path)
    data = req.read()
    file_ = open(filename, 'w')
    file_.write(data)
    file_.close()

fname='April2015.xls'
xls = pandas.ExcelFile(fname)
data=xls.parse(skiprows=2)
print(data)
