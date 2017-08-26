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

def get_clinical_research(medicament):
    page = html.parse(urlopen('https://www.rlsnet.ru/tn_alf_letter_c0.htm'))
    
    e = page.getroot().\
        find_class('search__filter')
    
    links = []

    # Create a dictionary of links.
    for i in e:   
        d = {'key': i.text_content(), 'value': i.attrib.get("href")}
        links.append(d)
    
    link_togo = ''
    
    # Find a link for transition.
    for i in links:
        if medicament[0].upper() == i['key']:
            link_togo = i['value']    
      
    link_togo = "https:" + link_togo
    
    print(link_togo)
    page = html.parse(urlopen(link_togo))  
 
    #'tn_alf_list'
    e = page.getroot().\
        find_class('alphabet__delimiter')

    # Create a dictionary of links.
    for i in e:   
        d = {'key': i.text_content(), 'value': i.attrib.get("id")}
        links.append(d)
    print(links)
    med = medicament.upper()
    print(med)
    # Find a link for transition.
    for i in links:
        print(i['key'].upper())
        if medicament.upper() == i['key'].upper():
            print(i['key'].upper())
            link_togo = i['value']
    print(link_togo)

    mapping = {
            'page': link_togo
        }

    body = render("view", mapping)
    return body
'''
print(link_togo)
    page = html.parse(urlopen(link_togo))  
 
    #'tn_alf_list'
    e = page.getroot().\
        find_class('tn_alf_list')

    # Create a dictionary of links.
    for i in e:   
        d = {'key': i.text_content(), 'value': i.attrib.get("href")}
        links.append(d)
    
    med = medicament.upper()
    print(med)
    # Find a link for transition.
    for i in links:
        if medicament.upper() == i['key'].upper():
            link_togo = i['value']
    print(link_togo)



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
