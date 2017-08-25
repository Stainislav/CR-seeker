#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os.path
from string import Template
from templating import render
from cgi import parse_qs, escape
import lxml.html as html
from pandas import DataFrame

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

def get_clinical_research():
    page = html.parse(urlopen('https://www.rlsnet.ru/tn_alf_letter_c0.htm'))
    
    e = page.getroot().\
        find_class('search__filter')
    
    links = []
       
    for i in e:
        #links = links + i.attrib.get("href")
        links.append(i.attrib.get("href"))
   
    mapping = {
            'page': links
        }

    body = render("view", mapping)
    return body
'''
broken_html = "https://www.rlsnet.ru/tn_alf_letter_c0.htm"

    parser = etree.HTMLParser()
    tree   = etree.parse(StringIO(broken_html), parser)

    page = etree.tostring(tree.getroot(),
                            pretty_print=True, method="html")

 #myString = "https://www.rlsnet.ru/tn_alf_letter_c0.htm"
    #page = etree.parse(StringIO(myString))
#"<html><head><title>test<body><h1>page title</h3>"
'''
'''
    e = page.getroot().\
        find_class('search__alphabet').\
        pop()



    url_list = ''

    for i in e:
        url_list = url_list + i
    print(url_list)

    #page = page.getroot()
    #page = page.text_content()
    
    #t = e.getchildren().pop()
    #t = t.text_content()
    
    alphabet = ''
       
    for i in e:
        alphabet =  alphabet + i.text_content()
   
    mapping = {
            'page': alphabet
        }

    #"html/aironepage/HTML/index.html"
  '''