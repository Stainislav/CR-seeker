#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
from string import Template

def render_string(string, dictionary):
    result = string % dictionary
    return result

def render(templatename, mapping):

    direction = '/home/stanislav/Dropbox/Programming/CS50/final_project/CR-seeker.git/templates/'     
    tpath = direction + templatename
    h = open(tpath, 'r')
    template = h.read()
    h.close()

    return render_string(template, mapping)
    
