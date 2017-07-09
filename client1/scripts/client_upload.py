#!/usr/bin/python2

import cgi

print "content-type: text/html"
print
print "/nhello"
fileData=cgi.FormContent()['f'][0]

fh=open('data.txt','w')
fh.write(fileData)
fh.close()
