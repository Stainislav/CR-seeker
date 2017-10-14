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


# The Russia Medicines Registry (RMR).
BASE_URL = 'https://www.rlsnet.ru/tn_alf_letter_c0.htm'

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

def error(search_error):
    default_msg = 'Данный препарат отсутствует в реестре лекарственных средств России'

    if len(search_error) < 1:
        search_error = default_msg

    mapping = {
        'page': search_error    
    }

    body = render('search_error', mapping)
        
    return body

def choose_medicament(medicament_list):
    mapping = {
        'page': medicament_list
    }
    body = render("choice", mapping)
    return body

def parse(html):
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find('div', class_='alphabet__current')    
    
    links = []
   
    # Create a dictionary of links and alphabet letters.
    for i in div.find_all('a')[0:29]:
        d = {'key': i.text, 'value': i['href']}
        links.append(d) 

    return links

def parse_pharm_group(html):
    soup = BeautifulSoup(html, "html.parser")
    
    homeopathy_page = soup.find('table', class_='rest_nest')
    homeopathy_list = homeopathy_page.find_all('a')
    
    #pharm_group = soup.find('div', class_="drug__content")
    #name_of_pharm = pharm_group.find('a', class_="drug__link drug__link--article")
    return name_of_pharm.text

def get_active_substance():
    pass

def is_homeopathy(pharm_group):
    homeopathy = 'ГОМЕОПАТ'
    result = re.findall(homeopathy, pharm_group.upper())    

    if result:
        return True
    else: 
        return False    

def parse_medicament(html):
    soup = BeautifulSoup(html, "html.parser")
    medicament = soup.find('div', class_='tn_alf_list')
    
    links = []

    # Create a dictionary of medicament lists.
    for i in medicament.find_all('a'):
        d = {'key': i.text, 'value': i['href']}
        links.append(d) 
    
    return links

def get_medicament_name():
    pass

def pubmed_parse(medicament):
    
    # Get NCBI page.
    # clinical_link = 'https://www.ncbi.nlm.nih.gov/pubmed/clinical?term='
    # url = clinical_link + medicament
    # researches = get_html(url)   
    # soup = BeautifulSoup(researches, "html.parser")
    # return reviews
    pass
   
def parse_clinical_trials(html):
    soup = BeautifulSoup(html, "html.parser")
    
    clinical_html = soup.find('div', class_='main__content')
    clinical_key = re.search("клинич+..... (?=исследов)", str(clinical_html), flags=re.IGNORECASE)
        
    print('clinical_key: ', clinical_key)
    
    if clinical_key == None:
        print("КЛИНИЧЕСКИЕ ИССЛЕДОВАНИЯ ОТСУТСТВУЮТ!")
    else:
        print("КЛИНИЧЕСКИЕ ИССЛЕДОВАНИЯ ОБНАРУЖЕНЫ!!!")
    # return None if there is no matches    
    return clinical_key

def get_clinical_research(medicament):
    
    # Get an alphabet characters list.
    alphabet_list = parse(get_html(BASE_URL))
    
    link_togo = ''

    # If user didn't input medicament, return an error.
    if len(medicament) < 1:
        body = error('')
        return body

    # Find a link for transition to the page with a particular letter.
    for i in alphabet_list:
        if medicament[0].upper() == i['key']:
            link_togo = i['value']
    
    # If there is no appropriate letter in the RMR, return an error.
    if len(link_togo) < 1:
        body = error('')
        return body

    # Make the link is working.
    link_togo = "https:" + link_togo
        
    # Parse a medicament page.
    medicament_html = get_html(link_togo)
    medicament_list = parse_medicament(medicament_html)
   
    medicament_link = []
    
    result = ''

    # Find the matches in the medicament list.
    for i in medicament_list:
        result = re.findall(medicament.upper(), i['key'].upper())
        if result:
            medicament_link.append(i['value'])
       
    # If we didn't find a particular medicament in the RMR, return an error.
    if len(medicament_link) < 1:
        body = error('')
        return body
    
    # If there is more than one search results, go to choose-template.        
    if len(medicament_link) > 1:
        body = choose_medicament(medicament_link)
        return body       
    
    # Go to the medicament page.
    link_togo = "https:" + medicament_link[0]
   
    medicament_page = get_html(link_togo)
    
    clinical_trials = parse_clinical_trials(medicament_page)
    
    mapping = {
        'page': medicament_page
    }
       
    body = render("view", mapping)
    return body
