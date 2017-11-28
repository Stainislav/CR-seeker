#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cgi import parse_qs, escape
from functions import index
from controller import get_clinical_research

#import sys
#sys.path.append('/home/Demiurge/CR-seeker/control')


def application(environ, start_response):
    
    path = environ['PATH_INFO']
    dictionary = parse_qs(environ['QUERY_STRING'])  
      
    medicament = dictionary.get('medicament',[''])[0]
    medicament  = escape(medicament)
    
    # Delete spaces in the end of the medicament name.
    medicament = medicament.rstrip()
        
    response_body =''
    status = ''
   
    if path == '/':
        status = '200 OK'
        response_body = index()
                   
    elif path == '/index':
        status = '200 OK'
        response_body = get_clinical_research(medicament)

    else:
        status = '404 NOT FOUND'
        response_body = 'Page not found.'
     
    headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(response_body)))
    ]

    start_response(status, headers)
    yield response_body.encode('utf-8')

