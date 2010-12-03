#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

# enable debugging
import Translator
import cgitb
import cgi

cgitb.enable()

print "Content-Type: text/plain;charset=utf-8"
print

# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
text = form.getvalue('text')

if text!= None:
  
    #x = Transliterate.Transliteration(Transliterate.ARABIC)
    #arabicText = x.getTransliteration(text).encode("UTF-8");
    arabicText = text
    print "English: "+  Translator.translate(arabicText) + "<br/>";
    print "Arabic: "+ arabicText 
    
else:
  print 'Please enter an 3arabi phrase. Example: "3arabi"'
