# -*- coding: iso-8859-1 -*-
from urllib2 import urlopen
from urllib import urlencode
import sys
#import Transliterate

GOOGLE_MAX_CHAR = 680;

def detect_lang(text):
  base_url="http://www.google.com/uds/GlangDetect?callback=google.language.callbacks.id100&"
  params=urlencode( (('v',2.0),('q',text)))
  url=base_url+params
  content=urlopen(url).read()
  start_idx=content.find('"language":"')+12
  language=content[start_idx:]
  end_idx=language.find('","')
  language=language[:end_idx]
  return language  


def translate(text):
  '''
  Returens a string with the translation
  '''
  paragraphs = text.split('\n')
  #lang1 = detect_lang(paragraphs[0][:600])#detects the langauge of the input, we don't need it here
  lang1 = "ar"
  lang="en" #destination language
  
  langpair = '%s|%s'%(lang1,lang)
  base_url = 'http://ajax.googleapis.com/ajax/services/language/translate?'

  translation = ''
  index = 0
  for p in paragraphs:
	  cut = False
	  index += 1
	  if len(p.strip()) < 1: continue
	  if len(p) > GOOGLE_MAX_CHAR: 
		  paragraphs.insert(index, p[GOOGLE_MAX_CHAR:])
		  p = p[:GOOGLE_MAX_CHAR]
		  cut = True
	  params = urlencode((('v',1.0), ('q',p),('langpair',langpair)))
	  url = base_url + params
	  content = urlopen(url).read()
	  start_idx = content.find('"translatedText":"')+18
	  _translation = content[start_idx:]
	  end_idx = _translation.find('"}, "')
	  translation += _translation[:end_idx]# + '\n'
	  if cut: newline = ''
	  else: newline = '\n'
	  
	  #translation+= _translation[:end_idx].replace('\u0026quot;', '"') + "\n"
  return translation
  
def arabiTranslate(text):
    #x = Transliterate.Transliteration(Transliterate.ARABIC)
    #arabicText = x.getTransliteration(text).encode("UTF-8");
    #print arabicText
    return translate(text)
    
if __name__ == "__main__":
  print arabiTranslate("3arabi")
