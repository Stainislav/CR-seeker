#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
import os.path
from string import Template
from templating import render
from cgi import parse_qs, escape
import lxml.html as html
#from pandas import DataFrame

DATABASE = '/home/stanislav/Dropbox/Programming/CS50/final_project/CR-seeker.git/data/database.db'
connection = sqlite3.connect(DATABASE)
db = connection.cursor()

def index():
    mapping = {}
    #"html/aironepage/HTML/index.html"
    body = render("index", mapping)
    return body
'''
def get_clinical_research():
    page = html.parse('https://www.rlsnet.ru/tn_alf_letter_c0.htm')

    mapping = {
            'page': page,
        }

    body = render("view", mapping)
    return body
'''
