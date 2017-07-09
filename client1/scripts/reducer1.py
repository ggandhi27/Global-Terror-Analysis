#!/usr/bin/python2

#import mapper1
import matplotlib.pyplot as plt
import numpy as np
import operator
import sys

a=sys.stdin
b=""
for x in a:
	b=x
#print b

lists=[]

b=b.split(':')

occurbar=[]
for x in b[0].split(','):
	occurbar.append(int(x))
#print occurbar

countrybar=[]
for x in b[1].split(','):
	countrybar.append(x)
#print countrybar


y_pos=np.arange(len(countrybar))
plt.bar(y_pos,occurbar,align='center',alpha=0.5)
plt.xticks(y_pos,countrybar)
plt.ylabel('number of attacks')
plt.title('Number of  attacks in countries')
plt.savefig('/client1/bar.png')

#plt.show()

