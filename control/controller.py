#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
from templating import render
from functions import error, get_html, parse_medicament, parse_clinical_trials, parse, get_first_letter_url, get_medicament_list, find_medicament_matches, check_input

# The Russia Medicines Registry (RMR) url.
BASE_URL = 'https://www.rlsnet.ru/tn_alf_letter_c0.htm'


def get_clinical_research(medicament):
    
    if check_input(medicament) == False:
        return error()

    # Get an alphabet characters list.
    alphabet_list = parse(get_html(BASE_URL))
    
    # Find a link for transition to the page with a particular letter.
    link_togo = get_first_letter_url(alphabet_list, medicament)
    
    if check_input(link_togo) == False:
        return error()
   
    # Get a list of medicaments.
    medicament_list = get_medicament_list(link_togo)

    # Get a list of medicaments that were find.
    medicament_link = find_medicament_matches(medicament_list, medicament)

    if check_input(medicament_link) == False:
        return error()

    # Create a bootstrap table to display data that was found.
    html = "  <table class='table table-hover'><thead class='thead-dark'><tr><th scope='col'>Страница препарата в регистре лекарственных средств России</th><th scope='col'>Информация о клинических исследованиях</th></tr></thead>"

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
