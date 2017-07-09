#import mapper2
import matplotlib.pyplot as plt
import numpy as np
#import operator
import sys
a=sys.stdin
b=""
for x in a:
	b=x


lists=[]

b=b.split(':')

year=[]
occur=[]
for x in b[0].split(','):
	year.append(int(x))
print year


for x in b[1].split(','):
	occur.append(int(x))
print occur

#print year
#print occur
plt.plot(year,occur)
plt.savefig('year.png')
#plt.show()
