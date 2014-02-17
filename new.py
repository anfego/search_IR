#this program reads one html file (URL predefined),
#extracts the words from the text content of the file,
#converts the words into lower case, 
#writes out the words to an output file.

import urllib2 
from BeautifulSoup import *
import re

#assume pages contain one page only for now
def crawl(pages, outfile):
    for page in pages:
        try:
            c=urllib2.urlopen(page)
        except:
            print "could not open the %s" % page
            continue

        soup = BeautifulSoup(c.read())

        #call code here to remove the html tags from the html file 
        #resulting in Unicode u'Hello'
        text = GetTextOnly(soup)

        #separate and stem the words
        words = SeperateWords(text)
        for w in words:
            outfile.write("%s\n" % str(w))
        
#remove all tags, return a list of words (one word per line)
#from the text content of the html file
def GetTextOnly(soup):
    v = soup.string
    if v==None:
        c = soup.contents
        resulttext = ''
        for t in c:
            subtext = GetTextOnly(t)
            resulttext +=subtext + '\n'
        return resulttext
    else:
        return v.strip()

def SeperateWords(text):
    output = []
    splitter = re.compile('\\W*')
    words = splitter.split(text)
    print words
    for s in words:
        if s!='':
           output.append(s.lower())
    return output


if __name__ == '__main__':
        
    outfile = open("result", "w")
    
    pages = ['http://www.mtsu.edu/~csdept/index.htm']
    crawl(pages, outfile)
   
    outfile.close()
