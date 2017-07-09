#!/usr/bin/python2
import commands as cmd

print  "content-type: text/html"
print

p=cmd.getstatusoutput("cat globalterrorismdb_0616dist.csv | python mapper2.py | python reducer2.py")

print ''' <html>
<iframe  src="/year.png" style="border-style: none; border-color: inherit; border-width: 0px; width: 1000px; height: 500px;">
</iframe>
<<br><br>
<a href="../client_choose.html">Back to Choose Option</a>
</html>'''
