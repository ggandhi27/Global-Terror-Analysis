#! /usr/bin/python2
import cgi
import commands

print "content-type: text/html"
print

code=cgi.FormContent()['code'][0]
print "hello"a

fh=open("../uploads/code.py", 'w')
fh.write(code)
fh.close()
commands.getstatusoutput("chmod +x /client1/uploads/code.py")
