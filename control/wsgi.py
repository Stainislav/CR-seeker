#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cgi import parse_qs, escape
from functions import index
from controller import get_clinical_research

# It is a crutch. I add it in the end of the string, because Google Chrome cuts the string otherwise.
BUFFER_CRUTCH = ' '


def application(environ, start_response):
    
    path = environ['PATH_INFO']
    dictionary = parse_qs(environ['QUERY_STRING'])  
 
    region = dictionary.get('region', [''])[0]
    clicked_id = dictionary.get('clicked_id', [''])[0]
    comments_to_delete = dictionary.get('comments_to_delete', [''])[0]     
    medicament = dictionary.get('medicament',[''])[0]
    medicament  = escape(medicament)
        
    response_body =''
       
    if path == '/':
        response_body = index()
               
    if path == '/index':
        response_body = get_clinical_research(medicament)
        
    # Add the crutch to the response body.
    crutch_buffer = BUFFER_CRUTCH * (len(response_body))
    response_body = response_body + crutch_buffer

    status = '200 OK'

    headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(response_body)))
    ]

    start_response(status, headers)
    return [response_body.encode('utf-8')]
