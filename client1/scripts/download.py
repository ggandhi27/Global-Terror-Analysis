#!/usr/bin/python2
import cgi
import commands as cmd
print "content-type: text/html"
print 

a=cmd.getoutput("hadoop fs -ls /")
a=a.split("\n")
print "<ul>"
for x in a[1:]:
        print "<li>"
        print x.split(" ")[-1]
        print "</li>"
print "</ul>"
