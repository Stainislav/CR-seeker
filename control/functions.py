#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from bs4 import BeautifulSoup
from templating import render

import urllib.request
from urllib.request import urlopen

# The Russian Medicament Registry (RMR).
BASE_URL = 'https://www.rlsnet.ru/tn_alf_letter_c0.htm'


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


def error(search_error):
    
    default_msg = 'Данный препарат отсутствует в регистре лекарственных средств России. Попробуйте продолжить поиск, изменив название.'
    
    error = ''
    if len(search_error) < 1:
        error = default_msg
    
    mapping = {
        'page': error    
    }

    body = render('index', mapping)
        
    return body


def choose_medicament(medicament_list):

    html = '<table>'
    for i in medicament_list:
        html = html + '<tr><td>' + i['key'] + ': ' + i['value'] + '</td></tr>' 
    html = html + '</table>'

    mapping = {
        'page': html
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
        
    # return None if there is no matches    
    return clinical_key

