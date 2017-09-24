#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os.path
from string import Template
from templating import render
from cgi import parse_qs, escape
import lxml.html as html
from pandas import DataFrame
import re

import urllib.request
from bs4 import BeautifulSoup

from io import StringIO
from lxml import etree

from urllib.request import urlopen

DATABASE = '/home/stanislav/Dropbox/Programming/CS50/final_project/CR-seeker.git/data/database.db'
connection = sqlite3.connect(DATABASE)
db = connection.cursor()

def index():
    mapping = {}
    body = render("index", mapping)
    return body

def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()

def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find('div', class_='alphabet__current')    
    
    links = []
   
    # Create a dictionary of links and alphabet letters.
    for i in div.find_all('a')[0:29]:
        d = {'key': i.text, 'value': i['href']}
        links.append(d) 

    return links
    
#def get_active_substance():

#def is_homeopathy():

def get_clinical_research(medicament):
    alphabet_list = parse(get_html('https://www.rlsnet.ru/tn_alf_letter_c0.htm'))
    
    link_togo = ''

    # Find a link for transition to the page with particular letter.
    for i in alphabet_list:
        if medicament[0].upper() == i['key']:
            link_togo = i['value']
     
    link_togo = "https:" + link_togo
    
 #   page = html.parse(urlopen(link_togo))  
  #  root = page.getroot()
   # tree = etree.ElementTree(root)

    #children = []
    #for e in tree.iter():
     #   d = {'key': e.text, 'value': e.attrib.get("href")} 
      #  children.append(d)
    
    mapping = {
            'page': link_togo
        }
   
    body = render("view", mapping)
    return body
