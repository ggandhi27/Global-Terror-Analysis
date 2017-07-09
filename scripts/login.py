#!/usr/bin/python2

import cgi
print "content-type: text/html"
print

userName=cgi.FormContent()['user'][0]
passWord=cgi.FormContent()['pass'][0[
