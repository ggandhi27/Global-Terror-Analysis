#!/usr/bin/python2

import cgi
import commands

print "Content-Type: text/html"
print 

nodeNum=cgi.FormContent()['nodesNum'][0]
'''
hostsStatus=cmd.getstatusoutput("echo y | cp /etc/ansible/hosts hosts ")
if hostsStatus[0]==0:
        hostsFile=open("hosts","a+")
        hostsFileData=hostsFile.read()
        hostsFile.seek(0)
        hostsFile.write(ansibleText)
        hostsFile.close()

masterAnsible="172.17.0.2 ansible_ssh_user=root"
hostsStatus=cmd.getstatusoutput("echo y | cp /etc/ansible/hosts hosts ")
if hostsStatus[0]==0:
        hostsFile=open("hosts","a+")
        hostsFileData=hostsFile.read()
        hostsFile.seek(0)
        hostsFile.write(masterAnsible)
        hostsFile.close()
'''
#commands.getoutput("yum install dhclient -y")
commands.getoutput("sudo ifconfig enp0s3 0")
commands.getoutput("sudo ifconfig docker0 0")
commands.getoutput("sudo brctl addif mybr enp0s3")
daemonfile="""
{
	"bridge": "mybr"
}
"""
hostfile=open("daemon.json","w")
hostfile.write(daemonfile)
hostfile.close()

#jt_ip=commands.getstatusoutput("docker inspect ar2 | jq .'[].NetworkSettings.Networks.bridge.IPAddress'")[1].strip('"')

#commands.getoutput("dhclient -v  eth0")
commands.getoutput("sudo systemctl restart docker")


commands.getoutput("docker run -dit --name=mapred_jt --privileged=true hadoop1:v1")
#commands.getoutput("docker exec mapred_jt ifconfig eth0 172.17.0.2"
commands.getoutput("docker cp /webcontent/scripts/daemon.json mapred_jt:/etc/docker/")
'''
hostsStatus=cmd.getstatusoutput("echo y | cp /etc/docker/daemon.json daemon.json ")
if hostsStatus[0]==0:
        hostsFile=open("daemon.json","a+")
        hostsFileData=hostsFile.read()
        hostsFile.seek(0)
        hostsFile.write(daemonfile)
        hostsFile.close()
'''
#commands.getoutput("dhclient -v  eth0")
#commands.getoutput("systemctl restart docker")
jt_ip=commands.getstatusoutput("docker inspect ar2 | jq .'[].NetworkSettings.Networks.bridge.IPAddress'")[1].strip('"')

commands.getoutput("sudo docker exec mapred_jt ifconfig eth0 0")
commands.getoutput("sudo docker exec mapred_jt dhclient -v eth0")


#commands.getoutput("docker cp /webcontent/mapred-site.xml mapred_jt:/etc/hadoop/")
dockerContent="<?xml version="1.0"?>\n<?xml-stylesheet type='text/xsl' href='configuration.xsl'?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>mapred.job.tracker</name>\n<value>{0}</value>\n</property>\n</configuration>".format(jt_ip)

mapredfile=open("mapred-site.xml","w")
mapredfile.write(dockerContent)
mapredfile.close()

commands.getoutput("sudo docker cp /webcontent/scripts/mapred-site.xml mapred_jt:/etc/hadoop/")


#commands.getoutput("docekr exec mapred_jobtracker ")
c=3
for i in range(0,int(nodeNum)):
	#print 
	dockerStart=commands.getstatusoutput("docker run -dit --name=mapred_tt_{} --privileged=true hadoop1:v1").format(c)
	if dockerStart[0] != 0:
		print "Error.. Try again"
	else:
		commands.getoutput("sudo docker cp /webcontent/mapred-site.xml mapred_tt_{}:/etc/hadoop/").format(c)
		commands.getoutput("sudo docker cp /webcontent/scripts/daemon.json mapred_jt:/etc/docker/")
		commands.getoutput("sudo docker exec mapred_jt ifconfig eth0 0")
		commands.getoutput("sudo docker exec mapred_jt dhclient -v eth0")
		c=c+1

	
