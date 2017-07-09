#! /usr/bin/python2
print  "content-type: text/html"
print

#cmd.getoutput("cat globalterrorismdb_0616dist.csv | python mapper1.py | python reducer1.py ")
print """
<html>
<iframe  src="/attacks.txt" style="border-style: none; border-color: inherit; border-width: 0px; width: 555px; height: 200px; margin: 120px 0 0 250px;">
</iframe>
<br><br>
<a href="../client_choose.html">Back to Choose Option</a>

</html>
"""

