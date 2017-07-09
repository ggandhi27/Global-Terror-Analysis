#! /usr/bin/python2
import cgi
import commands

print "content-type: text/html"
print

code=cgi.FormContent()['code'][0]
fileType=cgi.FormContent()['t'][0]
fileName=cgi.FormContent()['n'][0]
fh=open("{0}.{1}".format(fileName,fileType), 'w')
print "hello"
fh.write(code)
fh.close()
commands.getstatusoutput("chmod +x /client1/scripts/{0}.{1}".format(fileName,fileType))

#commands.getstatusoutput("hadoop jar /usr/share/hadoop/contrib/streaming/hadoop-streaming-1.2.1.jar -input passwd -mapper ./mapper.py -file mapper.py /reducer .reducer/reducer.py -file reducer.py -output /o5")
