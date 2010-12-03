# -*- coding: iso-8859-1 -*-
"""
Google Transliterate API
Public class:           Transliteration, TransliterationError
Public functions:       getTransliteration
"""

# Author: rajeshsr <srrajesh1989@gmail.com>
#         http://rajeshsr.co.cc
# Licensed under MIT License

import urllib2
import urllib
import re
#import json
import simplejson

class TransliterationError(Exception):
    pass

class Transliteration:

    _code = {
            'en':'ENGLISH',
            'ar':'ARABIC',
            'bn': 'BENGALI',
            'gu':'GUJARATI',
            'hi':'HINDI',
            'kn':'KANNADA',
            'ml':'MALAYALAM',
            'mr':'MARATHI',
            'ne':'NEPALI',
            'fa':'PERSIAN',
            'pa':'PUNJABI',
            'ta':'TAMIL',
            'te':'TELUGU',
            'ur':'URDU'
            }
    _headerData = {'Host' :  'www.google.com',
            'User-Agent' :  'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.14) Gecko/2009091010 Iceweasel/3.0.6 (Debian-3.0.6-3)',
            'Accept' :  'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language' : 'en-us,en;q=0.5',
            'Accept-Encoding' : 'gzip,deflate',
            'Accept-Charset' :  'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
            'Keep-Alive' :  '300',
            'Connection' :  'keep-alive',
            'Content-Type' :  'application/x-www-form-urlencoded;charset=utf-8',
            'Referer' : 'http://www.google.com/transliterate/',
            'Content-Length' :  '389',
            'Pragma' :  'no-cache',
            'Cache-Control' :  ' no-cache'}


    _postData = {
            'langpair' :  'ar|en',
            'num' : '5',
            'text' :   'vallamai',
            'tl_app' :  '3',
            'tlqt' :  '  1',
            'version' : '2',
            }
						

#pass destination language in constructor
    def __init__(self,dest = 'ta'):
        if dest not in self._code:
            raise TransliterationError, "Destination language %s not supported"%dest
        self._dest = dest
        self._postData['langpair'] = 'en|%s'%dest
        self._cache = {}
        #google caches some commonly used words by the following URL and use it to speed up. You can use this cache for offline transliteration too
        try:
            url = 'http://www.google.com/transliterate/indic?tlqt=4&langpair=en|%s&tl_app=3&v=1'%dest
            page = urllib.FancyURLopener({}).open(url).read()
            page = page.replace('\'','\"')
            self._cache = dict(zip(*simplejson.loads(page)))
        except Exception:
            #since this is just for optimization, don't bother if exception occurs
            pass


    def _getUnicode(self,s):
        """
        return the unicode string corresponding to the encoding in s
        """
        ans = u''
        m = re.compile('\\u([0-9a-fA-F]+)')
        return ans.join([unichr(int(x, 16)) for x in m.findall(s)])


    def _getTrans(self,word):
        if word == '':
            return u''
        if word in self._cache:
            return self._cache[word]
        dest = self._dest
        #param text contains the word to transliterate
        self._postData['text'] = word
        URL = 'http://www.google.com/transliterate/%s'%self._code[dest]
        req = urllib2.Request(URL,urllib.urlencode(self._postData))
        req.add_headers = (self._headerData.items())
        res = urllib2.urlopen(req)
        val = res.read()
        match = '"%s",\n\[\n"([^"]+)'%re.escape(self._postData['text'])
        matcher = re.compile(match)
        target = matcher.findall(val)
        if(len(target) == 0):
            raise TransliterationError, 'Unable to get transliteration of %s'%word
        self._cache[word] = self._getUnicode(target[0])
        return self._cache[word]


    def getTransliteration(self,line):
        """
        returns transliteration of line
        By default it is tamil
        """
        #Transliteration seems to return nothing with with non-(alphanumeric) characters, so sending only alphabet
        #Transliteration seems to be done even to numeric values. I don't see its utility yet. So only alpha-characters are sent.
        #Send word by word for transliteration as done by google transliterate itself. 
        stripped = ''
        ans = u''
        dest = self._dest
        for c in line:
            if not c.isalpha() and not c.isdigit():
                ans += self._getTrans(stripped) + c
                stripped = ''
            else:
                stripped += c
        ans += self._getTrans(stripped)
        return ans

#enums for passing destination language in constructor
ENGLISH = 'en'
ARABIC = 'ar'
BENGALI = 'bn'
GUJARATI = 'gu'
HINDI = 'hi'
KANNADA = 'kn'
MALAYALAM = 'ml'
MARATHI = 'mr'
NEPALI = 'ne'
PERSIAN = 'fa'
PUNJABI = 'pa'
TAMIL = 'ta'
TELUGU = 'te'
URDU = 'ur'



if __name__ == '__main__':
    x = Transliteration(ARABIC)
    print x.getTransliteration(inp).encode("UTF-8")
    '''
    while True:
        try:
            inp = raw_input()
            print x.getTransliteration(inp).encode("UTF-8")
        except EOFError:
            break 
     '''
     