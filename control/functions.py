#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
from templating import render

import urllib.request
from urllib.request import urlopen

# The Russian Medicament Registry (RMR).
BASE_URL = 'https://www.rlsnet.ru/tn_alf_letter_c0.htm'
default_msg = 'Данный препарат отсутствует в регистре лекарственных \
                   средств России. Попробуйте продолжить поиск, изменив название.'
HTTPS = 'https:'    

def index():
    variable = " "
    mapping = {
        'page': variable
    }
    body = render("index", mapping)
    return body


def get_html(url):
    response = urllib.request.urlopen(url)
    return response.read()


# Find a link for transition to the page with a particular letter.
def get_first_letter_url(alphabet_list, medicament):

    url = ''
     
    first_letter = medicament[0].upper()

    for i in alphabet_list:
        if first_letter == i['key']:
            url = i['value']

    if len(url) >= 1:
        url = HTTPS + url
        
    return url


def error(search_error=default_msg):
        
    mapping = {
        'page': search_error    
    }

    body = render('index', mapping)
        
    return body


def check_input(item):

    if len(item) < 1:
        return False
    else: 
        return True


def parse(html):

    soup = BeautifulSoup(html, "html.parser")
    div = soup.find('div', class_='alphabet__current')    
    
    links = []
   
    # Create a dictionary of links and alphabet letters.
    for i in div.find_all('a')[0:29]:
        d = {'key': i.text, 'value': i['href']}
        links.append(d) 

    return links


def get_medicament_list(url):

    medicament_html = get_html(url)
    medicament_list = parse_medicament(medicament_html)
    
    return medicament_list    


def parse_medicament(html):
    
    soup = BeautifulSoup(html, "html.parser")
    medicament = soup.find('div', class_='tn_alf_list')
    
    links = []

    # Create a dictionary of medicament lists.
    for i in medicament.find_all('a'):
        d = {'key': i.text, 'value': i['href']}
        links.append(d) 
    
    return links


def find_medicament_matches(medicament_list, medicament):

    medicament_link = []

    result = ''
    
    # Find the matches in the medicament list.
    for i in medicament_list:
        result = re.findall(medicament.upper(), i['key'].upper())
        if result:
            d = {'key': i['key'], 'value': i['value']}
            medicament_link.append(d)

    return medicament_link

   
def parse_clinical_trials(html):

    soup = BeautifulSoup(html, "html.parser")
    
    clinical_html = soup.find('div', class_='main__content')
    clinical_key = re.search("клинич+..... (?=исследов)", str(clinical_html), flags=re.IGNORECASE)
        
    # return None if there is no matches    
    return clinical_key

