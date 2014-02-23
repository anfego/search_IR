k#extracts the words from the text content of the file,
#converts the words into lower case, 
#writes out the words to an output file.

import urllib2 
from bs4 import *
from urlparse import urljoin
import re

global deep_cur

#assume pages contain one page only for now
def crawl(page, outfile, docId, stopwords, ):

    
    new_links = []
    try:
        c = urllib2.urlopen(page)
    except:
        page = urljoin(page,"index.html")
        try:
            print "RETRYING.... %s\n" % page
            c = urllib2.urlopen(page)
        except:
            print "could not open the %s" % page
            return new_links

    soup = BeautifulSoup(c.read())
    
    print(pages[docId])

    #call code here to remove the html tags from the html file 
    #resulting in Unicode u'Hello'
    # Only add links to craw if the deep < 2
    if deep_cur <= 2:
        new_links = GetChildlinks(soup);
    else:
        new_links = ["None"]
     
        
    
    text = GetTextOnly(soup);

    #separate and stem the words
    words = SeperateWords(text,stopwords)
    i = 0
    for w in words:
        outfile.write("%20s\t%s\t%s\n" % (str(w), str(docId), str(i)))
        i = i + 1
    return new_links

        
#remove all tags, return a list of words (one word per line)
#from the text content of the html file
def GetTextOnly(soup):
    
    v = soup.string
    if v==None:
        c = soup.contents
        resulttext = ''
        for t in c:
            subtext = GetTextOnly(t)
            # print(subtext)
            # findNumber = re.compile('^[0-9]+|\s[0-9]+')
            # if (findNumber.search(subtext) == None):  # the condition is true if w is NOT a number
                # print(subtext)
            resulttext +=subtext + '\n'
                
            
        return resulttext
    else:
        return v.strip()




# Returns all child link from the parent URL
def GetChildlinks(soup):

    links = []
    
    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        links.append(link.get('href'))
        # pages.append(link.get('href'))
        # print(len(pages))
        
    # print(links)
    # print(pages)

    return links;

def SeperateWords(text,stopwords):
    output = []
    splitter = re.compile('[\W][\']|[\'][\W]|[^\'0-9a-zA-Z]')
    words = splitter.split(text)
    
    for s in words:
        if s!='':
            # After separate words checks for terms starting with a number
            # and discart them
            findNumber = re.compile('^[0-9]+|\s[0-9]+')
            # the condition is true if s does NOT start with a number
            if (findNumber.search(s) == None):
                # Verify stopwords
                if not s.lower() in stopwords:
                    output.append(s.lower())
                    pass
    return output

if __name__ == '__main__':
        
    outfile = open("wordlist.txt", "w")
    pagesFile = open("documents.txt", "w")
    docId = 0
    pages = ['http://www.mtsu.edu/~csdept/index.htm']
    stopwords = []
    # pages = ['http://man7.org/linux/man-pages/man2/mmap.2.html']
    root = len(pages)
    # ensure extensions are suported
    deep_cur = 0;
    # open file with stop words and index them in a list
    f = open('stopwords','r')
    for line in f:
        stopwords.append(line.rstrip())
        
    f.close()

    
    while 1:
        # Checks of the extension of the link to procced
        # a = pages[docId].split(".")[-1]
        pagesFile.write("%s\t%s\n" % (str(docId), str(pages[docId])))
        for x in xrange(0,len(pages)):
            if x == docId:
                print "*\t%s" % pages[x]
            else:
                print pages[x]
            
        # if (a != "htm") and (a != "html") and (a != "txt"):
        #     pages[docId] = urljoin(pages[docId],"index.html")
        # pagesFile.write("%s\t%s\n" % (str(docId), str(pages[docId])))

        new_pages  = crawl(pages[docId],outfile, docId, stopwords)

        # print pages[docId]
        # print (new_pages)
        for page in new_pages:
            print "\t%s" % page
            if not page in pages:
                pages.append(page)
                pass
            else:
                print "\t\tPage Crawled %s\n" % page

        # pages = pages + new_pages
        # print(pages[docId])
        # checks the current deep in the URL's tree 
        # if all links in the current level had have been crawl 
        # increment the deep_cur
        # print("root")
        # print(root-docId-1)
        print ("deep_cur: %d\tDocId: %d\tPages: %d" % (deep_cur, docId, len(pages)))
        
        # print("docId")
        # print(docId)
        # print("len")
        # print(len(pages))rm
        print "---------------------------------------------------------\n"

        if docId >= len(pages)  or deep_cur >= 3:
            print "EXIT"
            break
        if (root-docId) <= 1:
            root = len(pages)
            deep_cur = deep_cur + 1
        docId = docId + 1

                

        
    pagesFile.close()
    outfile.close()
