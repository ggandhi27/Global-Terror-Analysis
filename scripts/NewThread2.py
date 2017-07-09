#!/usr/bin/python2
from threading import Thread

print "Content-Type: text/html"
print 

def a(p,q):
	i=0
	while i<10:
		i+=1
		print	p

def b():
	i=0
	while i<10:
		i+=1
		print "bbbbbbbbbbbbbbb"


p1=Thread(target=a,args=(3,5))
p2=Thread(target=b,args=())
p1.start()
p2.start()
raw_input()
