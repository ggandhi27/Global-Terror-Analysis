#!/usr/bin/python2
import cgi
import commands as cmd
print "content-type: text/html"
print 
print "hiwda"

#getting thr number of task trackers 
ttf=open("TTNum.txt",'r')
tt_no=int(ttf.read()) 
ttf.close()

dt=open("dt.txt",'r')
result=dt.read()
dt.close()
print result
	
#getting ip and password of TT and JT from the html form

JT_Ansible=""
if result=="yes":
	#go to the file of ip's and passwords of the master and the slaves and fetch them to place them into te hosts file of ansible
	jt_Ip=cgi.FormContent()['jt_ip'][0]
	print jt_Ip
	jt_Pass=cgi.FormContent()['jt_pass'][0]
	print jt_Pass
	JT_Ansible=JT_Ansible+jt_Ip+" ansible_ssh_user=root ansible_ssh_pass="+jt_Pass
	print jt_Ip
	print JT_Ansible
	print "not knot"
	
	jtIpFile=open("/webcontent/scripts/JT_IP","w")
	jtIpFile.write(jt_Ip+','+jt_Pass)
	jtIpFile.close()
	ansibleText=JT_Ansible
	#copy the ip and password from the files of the slave 
	
	#store both JT and TT ip and password in the ansible file 
	
else:
	JT_Ansible="[job_tracker]\n"
	#getting the ip address and password of the jt from the html form
	jt_Ip=cgi.FormContent()['jt_ip'][0]

	jt_Pass=cgi.FormContent()['jt_pass'][0]
	JT_Ansible=JT_Ansible+jt_Ip+" ansible_ssh_user=root ansible_ssh_pass="+jt_Pass
	print "yo"
	jtIpFile=open("/webcontent/scripts/JT_IP","w")
	jtIpFile.write(jt_Ip+','+jt_Pass)
	jtIpFile.close()

	TT_Ansible="[task_tracker]\n"

	ipFile=open("/webcontent/scripts/mapred_ip.txt","w+")


	#list to store the ip addresses of the data nodes
	ipAddress=[]

	#list to store the respective root passwords of the data nodes
	ipPassword=[]

	for i in range(0,tt_no):
		ip=cgi.FormContent()["ip"+str(i)][0]
		ipPass=cgi.FormContent()["pass"+str(i)][0]
		ipPassword.append(ipPass)
		#writing ip address to the list
		ipAddress.append(ip)
		#writing ip and the password to the file
		ipFile.write(ip+','+ipPass+'\n')
	
		TT_Ansible=TT_Ansible+ip+" ansible_ssh_user=root ansible_ssh_pass="+ipPass+"\n"
	#closing the file
	ipFile.close()

	#text to be inserted into /etc/ansible/hosts
	ansibleText=JT_Ansible+"\n\n"+TT_Ansible
#hostsStatus=cmd.getstatusoutput("echo y | cp /etc/ansible/hosts hosts ")



hostsFile=open("hosts","w")
hostsFile.write(ansibleText)
hostsFile.close()
print "afterLLL"
mipf=open("masterIP",'r')
master_ip=mipf.read()
mipf.close()
print master_ip

#SEND THIS CORE FILE TO JOB TRACKER CORE FILE USING ANSIBLE
coreSiteFile='<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl"  href="configuration.xsl"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://{}:10001</value>\n</property>\n</configuration>'.format(master_ip)
#SEND THIS MAPRED FILE TO BOTH JB TRACKER AND TASK TRACKER 														
#Data that is to be inserted into the hdfs-site.xml file in /etc/hadoop folder for the master node
mapredFile='<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>mapred.job.tracker</name>\n<value>http://{}:9001</value>\n</property>\n</configuration>'.format(jt_Ip)


cmd.getstatusoutput("sudo iptables -F")
cmd.getstatusoutput("sudo setenforce 0")
jt_Ssh="sudo sshpass -p "+jt_Pass+" ssh -o stricthostkeychecking=no root@"+jt_Ip
print "voila"
c=cmd.getstatusoutput(jt_Ssh+" rpm -q jdk")
v=cmd.getstatusoutput(jt_Ssh+" rpm -q hadoop")

'''

checkjh="""
- hosts: all
  tasks:
   - copy:
      src: "jdk-7u79-linux-x64.rpm"
      dest: "/"
   - command: "sudo rpm -ivh jdk-7u79-linux-x64.rpm"

   - copy:
      src: "hadoop-1.2.1-1.x86_64.rpm"
      dest: "/"
   - command: "sudo rpm -ivh --replacefiles hadoop-1.2.1-1.x86_64.rpm"
"""
print "yolaa"
aFile=open("ans_jh.yml","w")
aFile.write(checkjh)
aFile.close()

if dt=="yes":
	pass
else:
	if c[0]==0:
		q=cmd.getstatusoutput("sudo ansible-playbook ans_jh.yml -i hosts")
	else:
		pass
print "<br /><br /><br />"
print q
'''	
#Creating files for core and hdfs to transfer on the remote system.
mapFile=open("mapred-site.xml","w")
mapFile.write(mapredFile)
mapFile.close()
#send this file to mapred folders of all the devices
coreFile=open("core-site.xml","w")
coreFile.write(coreSiteFile)
coreFile.close()
print "ola\n\n"
ans="""
---
- hosts: job_tracker
  tasks:
   - copy:
      src: "/webcontent/scripts/mapred-site.xml"
      dest: "/etc/hadoop/"
   - copy:
      src: "/webcontent/scripts/core-site.xml"
      dest: "/etc/hadoop/"
- hosts: task_tracker
  tasks:
   - copy:
      src: "/webcontent/scripts/mapred-site.xml"
      dest: "/etc/hadoop/"
"""

aFile=open("ans_jt.yml","w")
aFile.write(ans)
aFile.close()

print "\n\n"
p=cmd.getstatusoutput("sudo ansible-playbook ans_jt.yml -i hosts")
print p	

