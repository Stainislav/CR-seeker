#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from templating import render
from functions import error, get_html, parse_medicament, choose_medicament, parse_clinical_trials, parse

# The Russia Medicines Registry (RMR).
BASE_URL = 'https://www.rlsnet.ru/tn_alf_letter_c0.htm'


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
    
     # Delete spaces in the end of the medicament name.
    medicament = medicament.rstrip()

    result = ''
    
    # Find the matches in the medicament list.
    for i in medicament_list:
        result = re.findall(medicament.upper(), i['key'].upper())
        if result:
            d = {'key': i['key'], 'value': i['value']}
            medicament_link.append(d)
    
    # If we didn't find a particular medicament in the RMR, return an error.
    if len(medicament_link) < 1:
        body = error('')
        return body

    html = "  <table class='table table-hover'><thead class='thead-dark'><tr><th scope='col'>Страница препарата в регистре лекарственных средств России</th><th scope='col'>Информация о клинических исследованиях</th></tr></thead>"

#   html = "<table cellpadding='10' cellspacing='10'><td align='center' valign='top'><b>Название препарата</b></td><td align='center'><b>Информация о клинических исследованиях</b></td><td align='center'><b>Страница препарата в регистре лекарственных средств России</b></td>"

    search_result = ""
    warning = ""

    for i in medicament_link:
        link = "http:" + i['value']
        medicament_page = get_html(link)
        clinical_trials = parse_clinical_trials(medicament_page)

        if clinical_trials == None:
            search_result = 'Не найдена'
            warning = ""
        else:
            search_result = 'Найдена'
            warning = "class='table-primary'" 
    
        html = html + "<tr" + " " + warning + "><td align='left'><a href=" + "'" + link + "'" + " " + "target='_blank' class='text-dark'>" + i['key'] + "<a></td>" + "<td align='center'>" + search_result + "</td></tr>" 
    
    html = html + '</table>'

    mapping = {
        'page': html
    }
       
    body = render("index", mapping)
    return body
