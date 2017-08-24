#!/usr/bin/env python
# -*- coding: utf-8 -*-

from cgi import parse_qs, escape

from functions import index, get_clinical_research

def application(environ, start_response):
    
    path = environ['PATH_INFO']
    dictionary = parse_qs(environ['QUERY_STRING'])  
 
    region = dictionary.get('region', [''])[0]
    clicked_id = dictionary.get('clicked_id', [''])[0]
    comments_to_delete = dictionary.get('comments_to_delete', [''])[0]     

    response_body =''
       
    if path == '/':
        response_body = index()
               
    if path == '/index':
        response_body = get_clinical_research()
    
    status = '200 OK'

    headers = [
        ('Content-Type', 'text/html'),
        ('Content-Length', str(len(response_body)))
    ]

    start_response(status, headers)
    return [response_body.encode("utf-8")]

