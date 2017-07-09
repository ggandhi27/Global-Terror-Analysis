#!/usr/bin/python2
import cgi

print "content-type: text/html"
 

#import commands 
#import os
tt_no=cgi.FormContent()["tt_no"][0]
dt=cgi.FormContent()["dt"][0]


t_no= tt_no
t_no=int(t_no)

if t_no > 0  and t_no <= 10:
  #print "you are authenticated"
  print 
  TTNumFile=open("TTNum.txt","w")
  TTNumFile.write(tt_no)
  TTNumFile.close() 
  #print "hello world"
  #print "<a href="../form.html">click here to go to the form</a>"
else :
  #print "not authenticated"
  print "location: ../mapred-manual.html"
  print
  print "yo"

dtFile=open("dt.txt","w")
dtFile.write(dt)
dtFile.close() 

if dt=="yes":
	print "qwerty"
	
	print "<h1>Enter the IP Address and passwords of your mapred cluster systems.</h1><hr>"
	print '<form action="mapred_config.py" method="get">'
	print 'Ip Address for Job Tracker : <input type="text" name="jt_ip"> Root 		Password : <input type="password" name="jt_pass"><br><br>'
	print '<input type="submit" >'
	print "</form>"
	"""
	#set-Cookie: x=yes
	print "<html>"
	print '''<head>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="1; url=http://192.168.43.27/scripts/mapred_config.py">
        <script type="text/javascript">
            window.location.href = "http://192.168.43.27/scripts/mapred_config.py"
        </script>
        <title>Page Redirection</title>
    </head>'''
	print "<body>"	
	print  "If you are not redirected automatically, follow this <a href='http://192.168.43.27/scripts/mapred_config.py'>link to example</a>."
	print "</body>"
	print "</html>"
	"""
elif dt=="no":
	print "<html>"
	print "<body>"
	print "<h1>Enter the IP Address and passwords of your mapred cluster systems.</h1><hr>"
	print '<form action="mapred_config.py" method="get">'
	print 'Ip Address for Job Tracker : <input type="text" name="jt_ip"> Root Password : <input type="password" name="jt_pass"><br><br>'
	for i in range(0,int(tt_no)):
		print 'Ip Address for Task Trackers : <input type="text" name="ip%d"> Root Password : <input type="password" name="pass%d"><br><br>'%(i,i)

	print '<input type="submit" >'
	print "</form>"
	print "</body>"
	print "</html>"

else:
	pass
#print jt_pass
#print jt_ip
