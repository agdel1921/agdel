# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 09:37:55 2016

@author: Vidyut
"""

from __future__ import unicode_literals
import os
import sys  
reload(sys)  
sys.setdefaultencoding('utf8')
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import XMLConverter, HTMLConverter, TextConverter
from pdfminer.layout import LAParams
from cStringIO import StringIO

def pdfparser(data):
    dest = data[:-3]+"txt"    
    print "\n\n\n\n\n",dest    
    fp = file(data, 'rb')
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    # Create a PDF interpreter object.
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    # Process each page contained in the document.
    for page in PDFPage.get_pages(fp):
        interpreter.process_page(page)
        data =  retstr.getvalue()
        data = unicode(data,'utf-8', errors='ignore')
    #print data
    # write data to a file
    print data
    with open(dest, "w") as f:
        f.write(data)
    
# set the working directory
path = "F:/banking/payments/"
os.chdir(path)
fls=os.listdir(path)

for x in fls:
    if x[-3:]=="pdf":
        pdfparser(path+x)
        
