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
    return urllib2.urlopen(url, timeout=10).read()

def writefile(path, txt):
    open(path, "w").write(txt)

def synchtml(url,path):
    if os.path.exists(path):
        return open(path).read()
    else:
        html = readurl(url)
        writefile(path, html)
        return html

def get_links(html):
    linkpat = r'<a href="%s([^"#]*)["#]' % baseview
    return re.findall(linkpat, html)

def fetch_page(page, rev="current", recurse=False):
    print "getting", page
    #if not page.startswith('/'):
    abspage = baseview + page
    url = base + abspage
    relpath = "." + abspage
    if not os.path.exists(relpath):
        os.makedirs(relpath)

    try:
        rawuri = geturi(url, rawmode)
        rawpath = "%s/raw-%s" % (relpath, rev)
        synchtml(rawuri, rawpath)

        printuri = geturi(url, printmode)
        printpath = "%s/print-%s" % (relpath, rev)
        html = synchtml(printuri, printpath)
        links = get_links(html)
        html = None  # GC html

        visited.add(page)
        for link in links:
            if link not in visited:
                if recurse:
                    fetch_page(link, recurse=True)
                else:
                    print "link:", link
                    visited.add(page)
    except urllib2.URLError:
        visited.add(page)
        print >>sys.stderr, "timed out trying to read %s" % page

if sys.argv[1:]:
    for page in sys.argv[1:]:
        fetch_page(page, recurse=False)
else:
    #fetch_page("Documentation/Release3/NavAdminStorage")
    fetch_page(startpage, recurse=True)

