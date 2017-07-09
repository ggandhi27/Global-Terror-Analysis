#!/usr/bin/python2
import operator,sys
#f=open('globalterrorismdb_0616dist.csv','a+')
yearlist=[]
z=1
for i in sys.stdin:
	if z==1:
		z+=1
	        pass
	else:
	        yearlist.append(i.split(',')[1])


attacksperyear={}
for i in yearlist:
	if i in attacksperyear:
		attacksperyear[i]+=1
		
	else:
		attacksperyear[i]=1
year=[]
occur=[]
sorted_xx=sorted(attacksperyear.items(),key=operator.itemgetter(0))
#print sorted_xx
for i in sorted_xx:
	year.append(i[0])
	occur.append(str(i[1]))
#print year
#print occur

a=[]
for i in year:
	a.append(str(i))
a=','.join(year)
#print a		
b=[]
for i in occur:
	b.append(str(i))
b=','.join(occur)
#print b		
final=a+":"+b
print final




