#!/usr/bin/python2

print "Content-Type: text/html\n\n"

print 

import cgi
import commands as cmd
from threading import Thread

lock=0



def slaveConfiguration(ipAddress,ipPassword,username,Size,i,nfsIp):
	userId=str(i)+username
	print userId
	hdfsText='<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>dfs.data.dir</name>\n<value>/data%s%s</value>\n </property>\n</configuration>'%(str(i),username)
	hdfsFile=open("hdfs-site.xml","w")
	hdfsFile.write(hdfsText)
	hdfsFile.close()
	
	#tasks for ansible script
	#
	# 1 check for hadoop
	# 2 check for jdk
	# 3 make the partition
	# 4 mount the partition
	# 5 send the core site file
	# 6 send the hdfs site file
	# 7 start the services
	dataSsh="sudo sshpass -p "+ipPassword+" ssh -o stricthostkeychecking=no root@"+ipAddress

	java='''
   - copy:
      src: "jdk-7u79-linux-x64.rpm"
      dest: "/"
   - command: "sudo rpm -ivh jdk-7u79-linux-x64.rpm"
 
'''
	hadoop='''
   - copy:
      src: "hadoop-1.2.1-1.x86_64.rpm"
      dest: "/"
   - command: "sudo rpm -ivh --replacefiles hadoop-1.2.1-1.x86_64.rpm"

'''
	data = '''
- hosts: data%s
  tasks:
%s
%s
%s
   - copy:
      src: core-site.xml
      dest: /etc/hadoop/
   - copy:
      src: hdfs-site.xml
      dest: /etc/hadoop/
   - file:
      state: directory
      path: "/data%s"

   - command: "mount %s:/nfsshare%s /data%s"
   - command: "hadoop-daemon.sh stop datanode"
   - command: "hadoop-daemon.sh start datanode"

'''
	javaStatus=cmd.getstatusoutput(dataSsh+" rpm -q jdk")
	print javaStatus
	hdp=''
	jdk=''
        if javaStatus[0]==0:
		jdk=''
        else:
		jdk=java

	hadoopStatus=cmd.getstatusoutput(dataSsh+" rpm -q hadoop ")
	print hadoopStatus
        if hadoopStatus[0]==0:
		hdp=''
        else:
		hdp=hadoop
	#print ipAddress
	#print ipPassword
        bashStatus=cmd.getstatusoutput("sudo sshpass -p "+ipPassword+" scp root@"+ipAddress+":/root/.bashrc /FinalProject/scripts")
	#print bashStatus
	bashData='\nexport JAVA_HOME=/usr/java/jdk1.7.0_79/\nexport PATH=/usr/java/jdk1.7.0_79/bin/:$PATH\n'
        bashFile=open(".bashrc","a+")
        bashFile.write(bashData)
        bashFile.close()
	bash='''
   - copy :
      src: .bashrc
      dest: /root/
'''
	
	nfsText='''
---
- hosts: nfs
  tasks:
   - command: "lvcreate --size {1} --name lv{0} hadoopvg"
   - command: "mkfs.ext4 /dev/hadoopvg/lv{0}"
   - file:
      state: directory
      path: "/nfsshare{0}"
   - command: "mount /dev/hadoopvg/lv{0} /nfsshare{0}"
   - copy: 
      src: "exports"
      dest: "/etc/exports"
   - service:
      name: "nfs"
      state: started

'''.format(userId,str(Size))
	nfsFile=open("nfsansible.yml","w")
	nfsFile.write(nfsText)
	nfsFile.close()
	print "checkpoint 1"
	exportsFile=open("exports","a+")
	exportsFile.write("/nfsshare%s %s(rw,no_root_squash)\n"%(userId,ipAddress))
	print "checkpoint 2"
	exportsFile.close()
	data=data%(str(i),jdk,hdp,bash,userId,nfsIp,userId,userId)
	dataFile=open("data.yml","w")
	dataFile.write(data)
	dataFile.close()
	
	nfsStatus=cmd.getstatusoutput("sudo ansible-playbook nfsansible.yml -i /FinalProject/scripts/hosts")
	print nfsStatus
	dataStatus=cmd.getstatusoutput("sudo ansible-playbook data.yml -i /FinalProject/scripts/hosts")
	print dataStatus
	
	
	
def loop(ipAddress,ipPassword,username,nodeSize,nodesNum,nfsIp):
	print "inside the loop function."
	for  x in range(0,nodesNum):
		print x
		slaveConfiguration(ipAddress[x],ipPassword[x],username,nodeSize,x,nfsIp)
	

def masterConfiguration(masterIp,masterPass,username):
	print "Inside master configuration function"
	masterSsh="sudo sshpass -p "+masterPass+" ssh -o stricthostkeychecking=no root@"+masterIp

	java='''
   - copy:
      src: "jdk-7u79-linux-x64.rpm"
      dest: "/"
   - command: "rpm -ivh /jdk-7u79-linux-x64.rpm"
 
'''
	hadoop='''
   - copy:
      src: "hadoop-1.2.1-1.x86_64.rpm"
      dest: "/"
   - command: "rpm -ivh --replacefiles /hadoop-1.2.1-1.x86_64.rpm"

'''
	master = '''
- hosts: master
  tasks:
%s
%s
%s
   - copy:
      src: core-site.xml
      dest: /etc/hadoop/
   - copy:
      src: hdfs-site.xml
      dest: /etc/hadoop/
   - command: "hadoop-daemon.sh stop namenode"
   - command: "hadoop-daemon.sh start namenode"

'''
	javaStatus=cmd.getstatusoutput(masterSsh+" rpm -q jdk")
	hdp=''
	jdk=''
	print javaStatus
        if javaStatus[0]==0:
		jdk=''
        else:
		jdk=java

	hadoopStatus=cmd.getstatusoutput(masterSsh+" rpm -q hadoop ")
	print hadoopStatus
        if hadoopStatus[0]==0:
		hdp=''
        else:
		hdp=hadoop

        bashStatus=cmd.getstatusoutput("sudo sshpass -p "+masterPass+" scp root@"+masterIp+":/root/.bashrc /FinalProject/scripts")
	bashData='\nexport JAVA_HOME=/usr/java/jdk1.7.0_79/\nexport PATH=/usr/java/jdk1.7.0_79/bin/:$PATH\n'
	bashRc=cmd.getstatusoutput("sudo chown apache .bashrc")
        bashFile=open(".bashrc","a+")
        bashFile.write(bashData)
        bashFile.close()
	bash='''
   - copy :
      src: .bashrc
      dest: /root/
'''
	master=master%(jdk,hdp,bash)
	masterFile=open("master.yml","w")
	masterFile.write(master)
	masterFile.close()
	
	masterStatus=cmd.getstatusoutput("sudo ansible-playbook master.yml -i /FinalProject/scripts/hosts")
	print masterStatus

print "<h1>Wait while we are completing your installation.</h1>"
print "<img src=/load.gif height=100 width=100/>"
#opening file having number of data nodes and size of each data node
nodesNumFile=open("NodesNum","r")
nodeSizeFile=open("NodeSize","r")

nfsIpFile=open("nfsIP","r")
nfsPassFile=open("nfsPass","r")
nfsIp=nfsIpFile.read()
nfsPass=nfsPassFile.read()
nfsIpFile.close()
nfsPassFile.close()
nfsIp.strip("\n")
nfsPass.strip("\n")
nfsIp=nfsIp[0:len(nfsIp)-1]
nfsPass=nfsPass[0:len(nfsPass)-1]
username="gaurav"


#print "checkpoint 0"
exportsStatus=cmd.getstatusoutput("sudo sshpass -p "+nfsPass+"scp "+nfsIp+":/etc/exports /FinalProject/scripts")
#print exportsStatus
#print "checkpoint 1"


#reading the number of data nodes and the size of each data node
nodesNum=int(nodesNumFile.read())
nodeSize=float(nodeSizeFile.read())
#print "Checkpoint 2"


#closing the files
nodesNumFile.close()
nodeSizeFile.close()
#print cgi.FormContent()

masterAnsible="[master]\n"

#getting the ip address and password of the master from the html form
masterIp=cgi.FormContent()['masterip'][0]
masterPass=cgi.FormContent()['masterpass'][0]

masterAnsible=masterAnsible+masterIp+" ansible_ssh_user=root ansible_ssh_pass="+masterPass

#opening a file to save the ip address and password of master
masterIpFile=open("masterIP","w")
#writing data into the file
masterIpFile.write(masterIp+','+masterPass)

#closing the file
masterIpFile.close()


#opening the file to save the ip address and password of data node
ipFile=open("HDFS_ip","w+")

#list to store the ip addresses of the data nodes
ipAddress=[]

#list to store the respective root passwords of the data nodes
ipPassword=[]


dataAnsible="\n"
#loop to fetch the ip addresses and the passwords from the html form
for i in range(0,nodesNum):
	#fetching ip
	ip=cgi.FormContent()["ip"+str(i)][0]
	#fetching password
	ipPass=cgi.FormContent()["pass"+str(i)][0]
	#writing password to the list
	ipPassword.append(ipPass)
	#writing ip address to the list
	ipAddress.append(ip)
	
	#writing ip and the password to the file
	ipFile.write(ip+','+ipPass+'\n')
	
	dataAnsible=dataAnsible+"[data"+str(i)+"]\n"+ip+" ansible_ssh_user=root ansible_ssh_pass="+ipPass+"\n"
#closing the file
ipFile.close()

#text to be inserted into /etc/ansible/hosts
ansibleText=masterAnsible+"\n\n"+dataAnsible+"\n[nfs]\n"+nfsIp+" ansible_ssh_user=root ansible_ssh_pass="+nfsPass
print ansibleText
hostsFile=open("hosts","w")
hostsFile.write(ansibleText)
hostsFile.close()





#Data that is to be inserted into the core-site.xml file in /etc/hadoop folder for the master node
coreSiteFile='<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>fs.default.name</name>\n<value>hdfs://%s:10001</value>\n</property>\n</configuration>'%masterIp




#Data that is to be inserted into the hdfs-site.xml file in /etc/hadoop folder for the master node
hdfsSiteFile='<?xml version="1.0"?>\n<?xml-stylesheet type="text/xsl" href="configuration.xsl"?>\n<!-- Put site-specific property overrides in this file. -->\n<configuration>\n<property>\n<name>dfs.name.dir</name>\n<value>/master</value>\n </property>\n</configuration>'

#no need to make the /master file. It will be created automatically when the name node will be formatted.


#Creating files for core and hdfs to transfer on the remote system.
hdfsFile=open("hdfs-site.xml","w")
coreFile=open("core-site.xml","w")
hdfsFile.write(hdfsSiteFile)
coreFile.write(coreSiteFile)
hdfsFile.close()
coreFile.close()


#########################################################
#							#
#	Steps to be done using ansible			#
#							#
#	1. check for java if not present the install	#
#	2. check for hadoop if not present then install	#
#	3. set the path variable			#
#	4. send the hdfs-site and 			#
#	   the code-site files on the remote system	#
#	5. start the services on the remote system	#
#							#
#########################################################


print "Starting the thread"
#thread.start_new_thread(masterConfiguration,(masterIp,masterPass))
p1=Thread(target=masterConfiguration, args=(masterIp,masterPass,username))
p1.start()

print "Running the main thread"
nfsQuery="sudo sshpass -p "+nfsPass+" ssh -o stricthostkeychecking=no root@"+nfsIp
#the name of the vg on the remote server is supposed to be "hadoopvg"
#check for space
spaceQuery=nfsQuery+"  vgs -o vg_name,vg_size,vg_free --separator , --unit g --noheadings hadoopvg"
nfsStatus=cmd.getstatusoutput(spaceQuery)
print nfsStatus
freeSpace=None
if nfsStatus[0]==0:
	vgDetails=nfsStatus[1].split(",")
	print nfsStatus
        freeSpace=float(vgDetails[-1].strip("g"))
	print freeSpace
	if freeSpace<(nodeSize*nodesNum):
		print "Space is not available."
	else:
		print "space is available."
		p1=Thread(target=loop, args=(ipAddress,ipPassword,username,nodeSize,nodesNum,nfsIp))
		p1.start()
else:
	#print nfsStatus
	print "nfs status failed"


#########################################################
#							#
#	Tasks for the data node.			#
#							#
#	1. make partition				#
#	2. format the partition				#
#	3. mount the partition				#
#	4. make the hdfs-file.				#
#	5. send the core and hdfs file.			#
#	6. start the service				#
#							#
#########################################################
