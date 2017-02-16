#!/usr/bin/python

import urllib2
import sys
import os
import re

base      = "https://twiki.opensciencegrid.org"
baseview  = "/bin/view/"
startpage = "Main/WebHome"

printmode = {'cover': 'print'}
rawmode   = {'raw'  : 'on'}

visited = set()

def geturi(url, qq):
    qstr = '&'.join("%s=%s" % kv for kv in qq.items())
    return "%s?%s" % (url, qstr)

def readurl(url):
    return urllib2.urlopen(url).read()

def writefile(path, txt):
    open(path, "w").write(txt)

def get_links(html):
    linkpat = r'<a href="%s([^"#]*)["#]' % baseview
    return re.findall(linkpat, html)

def fetch_page(page, rev="current"):
    print "getting", page
    #if not page.startswith('/'):
    abspage = baseview + page
    url = base + abspage
    relpath = "." + abspage
    if not os.path.exists(relpath):
        os.makedirs(relpath)

    rawuri = geturi(url, rawmode)
    rawpath = "%s/raw-%s" % (relpath, rev)
    html = readurl(rawuri)
    writefile(rawpath, html)

    printuri = geturi(url, printmode)
    printpath = "%s/print-%s" % (relpath, rev)
    html = readurl(printuri)
    writefile(printpath, html)

    visited.add(page)
    for l in get_links(html):
        if l not in visited:
            #fetch_page(page)
            print l

if sys.argv[1:]:
    for page in sys.argv[1:]:
        fetch_page(page)
else:
    #fetch_page("Documentation/Release3/NavAdminStorage")
    fetch_page(startpage)

