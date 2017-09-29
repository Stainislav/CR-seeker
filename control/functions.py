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
    pharm_group = soup.find('div', class_="drug__content")
    name_of_pharm = pharm_group.find('a', class_="drug__link drug__link--article")
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

    # Create a dictionary of links and alphabet letters.
    for i in medicament.find_all('a'):
        d = {'key': i.text, 'value': i['href']}
        links.append(d) 
    
    return links

def get_clinical_research(medicament):
    alphabet_list = parse(get_html('https://www.rlsnet.ru/tn_alf_letter_c0.htm'))
    
    link_togo = ''

    # Find a link for transition to the page with particular letter.
    for i in alphabet_list:
        if medicament[0].upper() == i['key']:
            link_togo = i['value']    
     
    link_togo = "https:" + link_togo

    medicament_html = get_html(link_togo)

    medicament_list = parse_medicament(medicament_html)

    medicament_link = []

    for i in medicament_list:
        result = re.findall(medicament.upper(), i['key'].upper())
        if result:
            medicament_link.append(i['value'])
    
    if len(medicament_link) > 1:
        body = choose_medicament(medicament_link)
        return body       
    
    # Go to the medicament page
    link_togo = "https:" + medicament_link[0]
   
    medicament_page = get_html(link_togo)
    
    pharm_group = parse_pharm_group(medicament_page)

    if is_homeopathy(pharm_group) == True:
        print("Алярма! Гомеопатия!")

    # active_substance = get_active_substance(medicament_page)

    mapping = {
        'page': medicament_page
    }
       
    body = render("view", mapping)
    return body

            
    #link_togo = "https:" + medicament_link
    #здесь нужна функция для захода на страницу препарата
   # pharm_group = parse_pharm_group(get_html(link_togo))

    #is_homeopahty = ishomeopathy(pharm_group)
    #if is_homeopathy == True:
        #Здесь нужна функция, которая вместо принта будет выводить шаблон страницы с предупреждением о том, что препарат гомеопатический
     #   print('Это гомеопатический препарат. Следовательно, у него не может быть доказанной клинической эффективности')
   # find_trials
    # Сейчас функция parse выдаёт список словарей [{'ключ': 'А', 'значение: '//www.rlsnet.ru/tn_alf_letter_c0.htm'}]
    # Далее необходимо заходить на нужную страницу и добираться до инфы о препарате. 
    # Парсить инфу о фарм. группе и клинических исследованиях.
 #   page = html.parse(urlopen(link_togo))  
  #  root = page.getroot()
   # tree = etree.ElementTree(root)

    #children = []
    #for e in tree.iter():
     #   d = {'key': e.text, 'value': e.attrib.get("href")} 
      #  children.append(d)
    
