#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from string import Template

def render_string(string, dictionary):
    result = string % dictionary
    return result

def render(templatename, mapping):

    direction = '/home/stanislav/Dropbox/Programming/CS50/final_project/CR-seeker.git/templates/'
    #direction = '/home/stanislav/Dropbox/Programming/CS50/final_project/CR-seeker.git/templates/bootstrap-4.0.0-alpha.6/docs/examples/cover/'     
    tpath = direction + templatename
    h = open(tpath, 'r')
    template = h.read()
    h.close()

    return render_string(template, mapping)
    
