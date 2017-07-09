#!/usr/bin/python2
import cgi
import Cookie
print "Content-Type: text/html"
print 

nodesNum=cgi.FormContent()["nodesNum"][0]
nodeSize=cgi.FormContent()["nodeSize"][0]
#nodesNum=raw_input()
#nodeSize=raw_input()



print "<html>"
print "<body>"
print "<h1>Welcome To the World Of Hadoop.</h1><hr>"
print '<form action="hdfs_config.py" method="get">'
print 'Ip Address for Master node : <input type="text" name="masterip"> Root Password : <input type="password" name="masterpass"><br><br>'
for i in range(0,int(nodesNum)):
	print 'Ip Address for Data node : <input type="text" name="ip%d"> Root Password : <input type="password" name="pass%d"><br><br>'%(i,i)

print '<input type="submit" >'
print "</form>"
print "</body>"
print "</html>"
nodesNumFile=open("NodesNum","w")
nodesNumFile.write(nodesNum)
nodesNumFile.close()

nodeSizeFile=open("NodeSize","w")
nodeSizeFile.write(nodeSize)
nodeSizeFile.close()
