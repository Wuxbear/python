# -*- coding: utf-8 -*-
import sys
import re

def parse_setup(data):
    '''
    Parse data that start with [Item] string, end with space line.
    The "#"  mean comment mark, line start with comment will be ignore.
    key and value, split by "=" symbol.
    watch out the space before/after "=" symbol may be split into value.

    Example:
    [Item1]
    key1=value1
    key2=value2

    [Item2]
    key1=value1
    key2=value2
    '''
    META_DATA = {}
    dev_data = {}
    start = False

    for line in data:
        line = line.strip()
        match = re.search(r'\[.*\]',line)
        if line.startswith('#'):
            continue
        
        if not len(line) or line == data[-1] or match:
            if start:
                x = dev_data.copy()
                META_DATA[dict_index] = x
                dev_data.clear()
            start = False
            
        if start:
            strbuf = line.split('=')
            dev_data[strbuf[0]] = strbuf[1]
                            
        if match:
            dict_index = match.group()[1:-1]
            start = True
               
    return META_DATA


with open('parse_test_data.txt','r') as f:
    data = f.readlines()
    Meta_data = parse_setup(data)
    print(Meta_data)
f.close()
