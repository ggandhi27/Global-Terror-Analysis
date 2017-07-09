#!/usr/bin/python2
import operator,sys
from collections import Counter
#f=open('globalterrorismdb_0616dist.csv','a+')
#f=open('finaldataset.csv','a+')

#f=open('attacks.txt','a+')
attacks=[]
for i in sys.stdin:
	s=i.split(',')
	if s[6]=='United States':
		attacks.append(s[13])

count_attacks=Counter(attacks)
output_list=[]
for i in count_attacks:
	output_list.append([i,count_attacks[i]])
#print output_list
ff=open('attacks.txt','a+')
ff.write("Terror attacks in USA\n")
for i in output_list:
	ff.write("%s : %d\n"%(i[0],i[1]))

ff.close()
'''
print attacks
d={}
for j in attacks:
	if j in d:
		d[i]+=1
		print d
	else:
		d[i]=1
		print d
		
		


lista=[]

for i in f:
	lista.append(i.split(',')[17])
print lista
for i in lista:
	print i
print "-------------------------------------------------------------"
a=dict()
for i in lista:
	if i in a:
		a[i]+=1
		
	else:
		a[i]=1

print a

#print attacks
attacktype=[]
occur=[]

sorted_x=sorted(attacks.items(),key=operator.itemgetter(1))
#print sorted_x
for i in sorted_x:
	attacktype.append(i[0])
	occur.append(i[1])
#print attacktype
#print occur

attackspercountry={}
for i in countrylist:
	if i in attackspercountry:
		attackspercountry[i]+=1
		
	else:
		attackspercountry[i]=1
'''
