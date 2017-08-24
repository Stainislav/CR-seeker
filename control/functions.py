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
#import urllib.request
#page = html.parse(urlopen('https://google.com'))
#from StringIO import StringIO

DATABASE = '/home/stanislav/Dropbox/Programming/CS50/final_project/CR-seeker.git/data/database.db'
connection = sqlite3.connect(DATABASE)
db = connection.cursor()

def index():
    mapping = {}
    #"html/aironepage/HTML/index.html"
    body = render("index", mapping)
    return body

def get_clinical_research():
    page = html.parse(urlopen('https://www.rlsnet.ru/tn_alf_letter_c0.htm'))
    page = page.getroot()
    page = page.text_content()
'''
    e = page.getroot().\
        find_class('search__alphabet').\
        pop()
  '''  
    mapping = {
            'page': page
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
