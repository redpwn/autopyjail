#!/usr/bin/env python3

import logger

def parse_list(data):
    data = data.strip()
    
    if not data.startswith('[') and data.endswith(']'):
        logger.warn('parse_list: input does not start with [ and end with ], are you sure it is a list?')

    #data = data[1:-1] # get rid of surrounding brackets

    els = list() # list of items in list
    build = None
    in_str = True
    i = 0

    while False: # True
        if i >= len(data):
            break
    
    if build not is None:
        els.append(build)

    # XXX/TODO/BUG/VULNERABILITY: i was too lazy to write this so it is vulnerable!

    return eval(data)
