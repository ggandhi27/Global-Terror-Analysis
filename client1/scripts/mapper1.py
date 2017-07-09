#code that print top 30 frequently occurred atacks in countries and display year versus number of attacks graph
#!/usr/bin/python2
import operator
import matplotlib.pyplot as plt
import numpy as np
import sys
#f=open('globalterrorismdb_0616dist.csv','a+')
countrylist=[]

for i in sys.stdin:
	countrylist.append(i.split(',')[6])
attackspercountry={}
for i in countrylist:
	if i in attackspercountry:
		attackspercountry[i]+=1
		
 	else:
		attackspercountry[i]=1
country=[]
occur1=[]

sorted_x=sorted(attackspercountry.items(),key=operator.itemgetter(1))
#print sorted_x
for i in sorted_x:
	country.append(i[0])
	occur1.append(i[1])
#print country
#print occur1
c=-1
reverse=[]
while c>-30:
	reverse.append(occur1[c])
	c-=1

cc=-1
reversee=[]

while cc>-30:
	reversee.append(country[cc])
	cc-=1
#print reverse
#print reversee
ff=open('top30','a+')
ff.write("Top 30 most frequently occured terrorist attacks in countries:")
for i,j in zip(reverse,reversee):
	ff.write("%d terrorist attacks in %s\n"%(i,j))

occurbar=[]
c=-1
while c>-8:
	occurbar.append(occur1[c])
	c-=1

a=[]
for i in occurbar:
	print type(i)
	a.append(str(i))

print a
a=','.join(a)
print a


#print occurbar
cc=-1
countrybar=[]
while cc>-8:
	countrybar.append(country[cc])
	cc-=1

#countrybar=','.join(countrybar)
b=[]
for i in countrybar:
	print type(i)
	b.append(str(i))

print b
b=','.join(b)
print b


final=a+":"+b
print final
'''

y_pos=np.arange(len(countrybar))
plt.bar(y_pos,occurbar,align='center',alpha=0.5)
plt.xticks(y_pos,countrybar)
plt.ylabel('number of attacks')
plt.title('Number of  attacks in countries')

plt.show()


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
		
#print attacksperyear
year=[]
occur=[]
sorted_xx=sorted(attacksperyear.items(),key=operator.itemgetter(0))
#print sorted_xx
for i in sorted_xx:
	year.append(i[0])
	occur.append(i[1])
#print year
#print occur
plt.plot(year,occur)
plt.savefig('year.png')

plt.show()


'''
