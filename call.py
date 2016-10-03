#!/usr/bin/python

from pdf_to_html_json import pdf_to_html_json
import sys

if len(sys.argv) > 2:
    pdf_to_html_json(sys.argv[1], sys.argv[2])
elif len(sys.argv) == 2:
    pdf_to_html_json(sys.argv[1])
else:
    print('Missing input file argument')
    
