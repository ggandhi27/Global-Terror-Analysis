#!/usr/bin/python2

import cgi
import commands
print "content-type: text/html"
print

fileData=cgi.FormContent()['f'][0]
print "<br><br>"
print "Your File  Has Been Successfully Uploaded"
print "<br><br>"
print "<a href= '../client_main.html'>GO BACK TO Main Page</a>"


fh=open("file.txt", 'w')
fh.write(fileData)
fh.close()
p=commands.getstatusoutput("sudo hadoop fs -put /client1/scripts/file.txt  /")
print p
