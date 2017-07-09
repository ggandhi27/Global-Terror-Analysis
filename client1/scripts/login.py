#! /usr/bin/python2


import cgi
import commands
print "content-type: text/html"
#print

userName=cgi.FormContent()['username'][0]
passWord=cgi.FormContent()['password'][0]

auser="admin"
apass="redhat"

cuser="client"
cpass="redhat"



if userName == auser and passWord == apass:
	#print "you are authenticated"
	print "location: ../index.html"
	print
elif userName == cuser and passWord == cpass:
	print "location: ../main.html"
	print
	
else:
	#print "not valid user"
	print "location: ../index.html"
	print
	print ''' 
	<script>
	alert("enter valid id and password")
	</script>
'''
