#this program reads one html file (URL predefined),
#extracts the words from the text content of the file,
#converts the words into lower case, 
#writes out the words to an output file.

import urllib2 
from bs4 import *
from urlparse import urljoin
import re
from collections import namedtuple
# Global array for stop words
stopwords = []
nDoc = 0
invIndex = {}



#assume pages contain one page only for now
def crawl(pages, outfile, docfile, stopwords, depth):
    for page in pages:
        # try to open a URL, if not succeed, 
        # try again with index.html at the end of the URL
        depth_Temp = depth;
        try:
            c = urllib2.urlopen(page)
        except:
            page = urljoin(page,"index.html")
            try:
                print "RETRYING.... %s\n" % page
                c = urllib2.urlopen(page)
            except:
                print "could not open the %s" % page
                return 0
        
        docfile.write("%d\t%s\n" % (depth, str(page)))

        soup = BeautifulSoup(c.read())

        #call code here to remove the html tags from the html file 
        #resulting in Unicode u'Hello'
        text = GetTextOnly(soup)
        nDoc =  1
        i = 0 
        #separate and stem the words
        words = SeperateWords( text, stopwords)
        for w in words:
            i += 1
            outfile.write("%20s\t%s\t%s\n" % (str(w), str(nDoc), str(i)))

        # get the links and crawl over them if deep < 2
        if depth_Temp < 2:
            links = GetChildlinks(soup)
            if len(links) > 0:
                depth_Temp += 1
                crawl(links, outfile, docfile, stopwords, depth_Temp)
                pass
            pass
        
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

# Returns all child link from the parent URL
def GetChildlinks(soup):

    links = []
    
    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        links.append(link.get('href'))
    return links;

def SeperateWords(text,stopwords):
    output = []
    docDict = {}
    splitter = re.compile('[\W][\']|[\'][\W]|[^\'0-9a-zA-Z]')
    words = splitter.split(text)
    wordPos = 0;
    for s in words:
        if s!='':
            # After separate words checks for terms starting with a number
            # and discart them
            findNumber = re.compile('^[0-9]+|\s[0-9]+')
            # the condition is true if s does NOT start with a number
            if (findNumber.search(s) == None):
                #if word is already indexed
                if not s in docDict:
                    # Verify stopwords
                    if not s.lower() in stopwords:
                        output.append(s.lower())
                        
                        docDict[s] = [wordPos]
                        
                        pass
                else:
                # the word exist in the dictionary
                    docDict[s].append(wordPos) 

                    
            wordPos += 1

    # getting both the keys and values at once
    for key,value in docDict.items():
        freq = len(docDict[key])
        # invIndex[key] = 
        # print "%d\t%s=%s" % (a,key,value)


    return output

def loadStopWords(stopFile):
    for line in stopFile:
        stopwords.append(line.rstrip())

    pass
if __name__ == '__main__':
        
    outfile = open("result", "w")
    docfile = open("docs", "w")
    
    pages = ['http://www.mtsu.edu/~csdept/index.htm','https://mail.python.org/pipermail/python-list/2002-July/131960.html']
    stopwordsFile = open('stopwords','r')
    stopwordsFile.close()

    crawl(pages, outfile, docfile, stopwords, 0)
   
    outfile.close()
    docfile.close()
